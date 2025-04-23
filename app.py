import requests
import gradio as gr
import os
import tempfile
import re
import logging

# ————— Agent Definitions —————
class FileTypeAgent:
    """
    Determines file type (python/javascript) based on filename or code content.
    """
    def detect_file_type(self, filename: str, code: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.py':
            return 'python'
        if ext == '.js':
            return 'javascript'
        # fallback: inspect content
        if 'def ' in code:
            return 'python'
        return 'javascript'

class CommentAgent:
    """
    Wraps Ollama-based commenting logic.
    """
    def __init__(self, api_url: str, model: str):
        self.api_url = api_url
        self.model   = model

    def generate_comments(self, code: str, language: str) -> str:
        return _generate_comments(code, language)

class CodeGenAgent:
    """
    Wraps Ollama-based code-generation logic.
    """
    def __init__(self, api_url: str, model: str):
        self.api_url = api_url
        self.model   = model

    def generate_code(self, request: str, language: str) -> str:
        return _generate_code_with_comments(request, language)

# ————— Ollama Wrappers —————
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL    = "llama3:latest"
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Helper to strip markdown code fences

def _strip_code_fences(text: str) -> str:
    text = text.strip()
    # Match fenced code block
    if text.startswith("```"):
        # remove all leading ``` lines
        lines = text.splitlines()
        # drop first line
        lines = lines[1:]
        # if last line is ``` drop it
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines)
    return text


def check_ollama_server():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        r.raise_for_status()
        return True, ""
    except Exception as e:
        logging.error("Ollama server check failed", exc_info=e)
        return False, str(e)


def call_chat_api(system_prompt: str, user_content: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_content}
        ],
        "stream": False
    }
    r = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("message", {}).get("content", "").strip()


def _generate_comments(code: str, language: str) -> str:
    ok, err = check_ollama_server()
    if not ok:
        return f"# Error: cannot reach Ollama: {err}\n{code}"

    system = (
        "You are an expert Python programmer. "
        if language.lower() == 'python' else
        "You are an expert JavaScript programmer. "
    )
    system += (
        "Add Google-style docstrings (Args/Returns) and inline comments (# …). "
        if language.lower() == 'python' else
        "Add JSDoc docstrings (@param/@returns) and inline comments (// …). "
    )
    system += "Do NOT change code structure—output ONLY the commented code."

    try:
        raw = call_chat_api(system, code)
        out = _strip_code_fences(raw).strip()
        if not out or out == code.strip():
            return f"# Error: Ollama returned no changes.\n{code}"
        return out
    except Exception as e:
        logging.error("Error in commenting API", exc_info=e)
        return f"# Error generating comments: {e}\n{code}"


def _generate_code_with_comments(request: str, language: str) -> str:
    ok, err = check_ollama_server()
    if not ok:
        return f"# Error: cannot reach Ollama: {err}"

    system = (
        "You are an expert Python programmer. "
        if language.lower() == 'python' else
        "You are an expert JavaScript programmer. "
    )
    if language.lower() == 'python':
        system += (
            "Generate code for the request, add Google-style docstrings and inline comments (# …). "
            "Output ONLY the commented code."
        )
    else:
        system += (
            "Generate code for the request, add JSDoc docstrings (@param/@returns) and inline comments (// …). "
            "Output ONLY the commented code."
        )

    try:
        raw = call_chat_api(system, request)
        return _strip_code_fences(raw).strip()
    except Exception as e:
        logging.error("Error in generation API", exc_info=e)
        return f"# Error generating code: {e}"

# ————— Gradio Interface —————
file_type_agent = FileTypeAgent()
comment_agent   = CommentAgent(OLLAMA_CHAT_URL, OLLAMA_MODEL)
code_agent      = CodeGenAgent(  OLLAMA_CHAT_URL, OLLAMA_MODEL)


def process_comment_only(file, code_input, language):
    if file:
        try:
            src = open(file.name, 'r', encoding='utf-8').read()
            name = os.path.splitext(os.path.basename(file.name))[0] + "_commented"
        except Exception as e:
            return f"Error reading file: {e}", None
    elif code_input and code_input.strip():
        src   = code_input
        match = re.search(r'(?:def|function)\s+(\w+)', src)
        name  = match.group(1) if match else "commented_code"
    else:
        return "Please upload a file or type code.", None

    file_lang = file_type_agent.detect_file_type(name, src)
    commented  = comment_agent.generate_comments(src, file_lang)
    return commented, name


def process_generate_code(request_input, language):
    if not (request_input and request_input.strip()):
        return "Please provide a request.", None
    gen   = code_agent.generate_code(request_input, language.lower())
    match = re.search(r'(?:def|function)\s+(\w+)', gen)
    name  = match.group(1) if match else "generated_code"
    return gen, name


def create_download_file(text, language, base):
    ext  = '.py' if language.lower()=='python' else '.js'
    safe = re.sub(r'[^0-9A-Za-z_]', '_', base)
    tmp  = tempfile.NamedTemporaryFile(mode='w', prefix=safe+'_', suffix=ext, delete=False, encoding='utf-8')
    tmp.write(text)
    tmp.close()
    return tmp.name

custom_css = """
.gradio-container { font-family:Arial; max-width:1400px; margin:auto; }
.gr-button { background:#3498db !important; color:#fff !important; }
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as app:
    gr.Markdown("# CodeMentor: Agent-Driven Code Commenting and Generation", elem_classes=["header"])
    with gr.Row():
        with gr.Column():
            file_in  = gr.File(file_types=['.py','.js'], label="Upload Code File")
            lang_sel = gr.Dropdown(['Python','JavaScript'], value='Python', label="Language")
            req_box  = gr.Textbox(label="Request Code (Prompt generation)", lines=2)
            code_box = gr.Code(label="Or Type Code to Comment", language="python", lines=10)
            with gr.Row():
                btn_gen = gr.Button("Generate Code")
                btn_com = gr.Button("Comment Only")
        with gr.Column():
            out_code = gr.Code(label="Output", language="python", lines=15, interactive=False)
            download = gr.File(label="Download")

    btn_gen.click(
        fn=lambda req, lang: (lambda text, base: (text, create_download_file(text, lang, base)))(*process_generate_code(req, lang)),
        inputs=[req_box, lang_sel],
        outputs=[out_code, download]
    )
    btn_com.click(
        fn=lambda f, c, l: (lambda text, base: (text, create_download_file(text, l, base)))(*process_comment_only(f, c, l)),
        inputs=[file_in, code_box, lang_sel],
        outputs=[out_code, download]
    )

if __name__ == "__main__":
    app.launch()
