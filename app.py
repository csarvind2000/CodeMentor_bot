import gradio as gr
import os
from pathlib import Path
from agents import FileTypeAgent, CommentAgent, CodeGenAgent

# Setup directories
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize agents
file_type_agent = FileTypeAgent()
comment_agent = CommentAgent()
code_gen_agent = CodeGenAgent()

def comment_code(file, code_input, filename, custom_prompt):
    """Process uploaded file or pasted code and add comments."""
    code = ""
    if file:
        filename = os.path.basename(file.name)
        with open(file.name, 'r') as f:
            code = f.read()
    elif code_input:
        code = code_input
        filename = filename or ('code.py' if 'def ' in code or 'class ' in code else 'code.js')

    # Detect file type
    file_type = file_type_agent.detect_file_type(filename, code)

    # Generate comments
    commented_code = comment_agent.generate_comments(code, file_type, custom_prompt or None)

    # Determine output filename with correct extension
    extension = '.py' if file_type == 'python' else '.js'
    base_name = os.path.splitext(filename)[0] if filename else 'code'
    output_filename = f"commented_{base_name}{extension}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    with open(output_path, 'w') as f:
        f.write(commented_code)

    return (
        commented_code,
        output_path,
        f"Download commented file: {output_filename}"
    )

def generate_code(request, file_type):
    """Generate code based on user request."""
    code = code_gen_agent.generate_code(request, file_type.lower())
    
    # Determine output filename
    extension = '.py' if file_type.lower() == 'python' else '.js'
    output_filename = f"generated_code{extension}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    with open(output_path, 'w') as f:
        f.write(code)

    return (
        code,
        output_path,
        f"Download generated file: {output_filename}"
    )

# Gradio interface
with gr.Blocks(css="""
    body {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        color: #1A237E;
        margin: 0;
        padding: 20px;
        box-sizing: border-box;
    }
    .gr-panel {
        background-color: #BBDEFB;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        border: 1px solid #90CAF9;
    }
    .gr-button {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        transition: transform 0.1s, box-shadow 0.2s;
    }
    .gr-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
    }
    .gr-textbox, .gr-file, .gr-dropdown {
        background-color: #FFFFFF;
        color: #1A237E;
        border: 1px solid #90CAF9;
        border-radius: 6px;
        font-size: 14px;
    }
    .gr-textbox textarea {
        height: 120px !important;
        resize: none;
    }
    .filename-textbox textarea {
        height: 50px !important;
        resize: none;
    }
    .output-textbox textarea {
        height: 180px !important;
        resize: none;
    }
    .gr-markdown h1 {
        font-size: 26px;
        margin: 0 0 16px;
        color: #1976D2;
    }
    .gr-markdown.description {
        font-size: 18px !important;
        margin: 0 0 12px;
        color: #1976D2;
    }
    .gr-tabs {
        background-color: #BBDEFB;
        border-radius: 8px;
        padding: 8px;
        border: 1px solid #90CAF9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .gr-tab {
        background-color: #90CAF9;
        color: #1A237E;
        border-radius: 6px;
        padding: 8px 16px;
        margin: 0 4px;
        transition: background-color 0.2s;
    }
    .gr-tab:hover {
        background-color: #64B5F6;
    }
    .gr-tab-selected {
        background-color: #2196F3;
        color: white;
    }
    .tab-container {
        display: flex;
        gap: 16px;
        height: 560px;
    }
    .input-column, .output-column {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .input-column {
        max-width: 50%;
    }
    .output-column {
        max-width: 50%;
    }
    .gr-file, .gr-textbox, .gr-dropdown, .gr-button {
        margin: 0 !important;
    }
    .gr-file label, .gr-textbox label, .gr-dropdown label {
        color: #1976D2;
        font-weight: 500;
    }
    .upload-file {
        height: 100px !important;
        width: 80% !important;
        margin: 0 auto !important;
    }
    .upload-file .gr-file-upload {
        background-color: #E3F2FD;
        border: 2px dashed #90CAF9;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
        transition: background-color 0.2s;
    }
    .upload-file .gr-file-upload:hover {
        background-color: #BBDEFB;
    }
    @media (max-width: 768px) {
        .tab-container {
            flex-direction: column;
            height: auto;
        }
        .input-column, .output-column {
            max-width: 100%;
        }
        .upload-file {
            width: 100% !important;
        }
    }
""") as demo:
    gr.Markdown("# CodeMentor: Agent-Driven Code Commenting and Generation")
    with gr.Tabs():
        with gr.TabItem("Comment Code"):
            gr.Markdown(
                "Upload a .py/.js file or paste code to add comments.",
                elem_classes=["gr-panel", "description"]
            )
            with gr.Row(elem_classes=["tab-container"]):
                with gr.Column(elem_classes=["input-column"]):
                    file_input = gr.File(
                        label="Upload File (.py or .js)",
                        elem_classes=["gr-file", "upload-file"]
                    )
                    code_input = gr.Textbox(
                        label="Or Paste Code",
                        lines=5,
                        elem_classes=["gr-textbox"]
                    )
                    filename_input = gr.Textbox(
                        label="Filename (optional, e.g., script.py)",
                        lines=2,
                        elem_classes=["gr-textbox", "filename-textbox"]
                    )
                    prompt_input = gr.Textbox(
                        label="Custom Prompt (optional)",
                        placeholder="Enter custom prompt for commenting, or leave blank for default.",
                        lines=2,
                        elem_classes=["gr-textbox"]
                    )
                    comment_button = gr.Button("Add Comments", elem_classes=["gr-button"])
                with gr.Column(elem_classes=["output-column"]):
                    output_code = gr.Textbox(
                        label="Commented Code",
                        lines=9,
                        elem_classes=["gr-textbox", "output-textbox"]
                    )
                    output_file = gr.File(
                        label="Download Commented File",
                        elem_classes=["gr-file"]
                    )
                    output_message = gr.Markdown()

            comment_button.click(
                fn=comment_code,
                inputs=[file_input, code_input, filename_input, prompt_input],
                outputs=[output_code, output_file, output_message]
            )

        with gr.TabItem("Generate Code"):
            gr.Markdown(
                "Request code generation for Python or JavaScript.",
                elem_classes=["gr-panel", "description"]
            )
            with gr.Row(elem_classes=["tab-container"]):
                with gr.Column(elem_classes=["input-column"]):
                    request_input = gr.Textbox(
                        label="Code Request",
                        lines=5,
                        placeholder="e.g., Write a Python function to sort a list",
                        elem_classes=["gr-textbox"]
                    )
                    file_type_input = gr.Dropdown(
                        label="File Type",
                        choices=["Python", "JavaScript"],
                        value="Python",
                        elem_classes=["gr-dropdown"]
                    )
                    generate_button = gr.Button("Generate Code", elem_classes=["gr-button"])
                with gr.Column(elem_classes=["output-column"]):
                    generated_code = gr.Textbox(
                        label="Generated Code",
                        lines=9,
                        elem_classes=["gr-textbox", "output-textbox"]
                    )
                    generated_file = gr.File(
                        label="Download Generated File",
                        elem_classes=["gr-file"]
                    )
                    generated_message = gr.Markdown()

            generate_button.click(
                fn=generate_code,
                inputs=[request_input, file_type_input],
                outputs=[generated_code, generated_file, generated_message]
            )

demo.launch()