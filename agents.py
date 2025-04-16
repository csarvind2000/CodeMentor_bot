import os
import requests
from pathlib import Path
import re

class FileTypeAgent:
    def detect_file_type(self, filename: str, code: str) -> str:
        """Detect if the input is Python or JavaScript based on extension or content."""
        if filename.endswith('.py'):
            return 'python'
        elif filename.endswith('.js'):
            return 'javascript'
        else:
            # Fallback: Analyze code content
            if 'def ' in code or 'class ' in code or '#' in code:
                return 'python'
            elif 'function ' in code or 'const ' in code or '//' in code:
                return 'javascript'
        return 'unknown'

class CommentAgent:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url

    def generate_comments(self, code: str, file_type: str, custom_prompt: str = None) -> str:
        """Generate comments for the given code using Ollama API."""
        if not custom_prompt:
            custom_prompt = (
                "Add comments to all functions, classes, and module-level docstrings "
                "in the following code using the reStructuredText docstring format for Python "
                "or JSDoc for JavaScript. Additionally, add inline comments for EVERY line of code "
                "(including individual statements) using '#' for Python or '//' for JavaScript. "
                "Ensure comments are clear, concise, and describe functionality. "
                "Return ONLY the complete code with comments, without any additional text, "
                "explanations, or notes."
            )

        if file_type == 'python':
            prompt = (
                f"{custom_prompt}\n\n"
                f"```python\n{code}\n```"
            )
        elif file_type == 'javascript':
            prompt = (
                f"{custom_prompt.replace('reStructuredText', 'JSDoc')}\n\n"
                f"```javascript\n{code}\n```"
            )
        else:
            return code

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json().get('response', code)
            # Extract code from response
            if result.startswith('```') and result.endswith('```'):
                result = result.split('\n', 1)[1].rsplit('\n', 1)[0]
            # Filter out non-code, non-comment lines
            lines = result.split('\n')
            filtered_lines = []
            for line in lines:
                stripped_line = line.strip()
                # Keep code, docstrings, and comments
                if (
                    stripped_line.startswith(('def ', 'class ', 'function ', 'const ', 'let ', 'var ')) or
                    stripped_line.startswith(('"""', '#', '//', '/**', '*', '*/')) or
                    stripped_line.endswith((':', '(', '{', '}', ');')) or
                    re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', stripped_line) or
                    re.match(r'^\s*return\s+', stripped_line) or
                    re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\(', stripped_line)
                ):
                    filtered_lines.append(line)
            result = '\n'.join(filtered_lines)
            return result.strip()
        except Exception as e:
            print(f"Error generating comments: {e}")
            return code

class CodeGenAgent:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url

    def generate_code(self, user_request: str, file_type: str = 'python') -> str:
        """Generate code based on user request using Ollama API."""
        prompt = (
            f"You are an expert {file_type} developer. Write {file_type} code based on the following request: "
            f"'{user_request}'. Ensure the code is well-structured, includes comments using "
            f"{'reStructuredText' if file_type == 'python' else 'JSDoc'} format for functions and modules, "
            f"and inline comments for EVERY line using '#' for Python or '//' for JavaScript. "
            f"Return ONLY the complete code, without any additional text, explanations, or notes.\n\n"
            f"```{file_type}\n\n```"
        )

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json().get('response', '')
            # Extract code from response
            if result.startswith('```') and result.endswith('```'):
                result = result.split('\n', 1)[1].rsplit('\n', 1)[0]
            # Filter out non-code, non-comment lines
            lines = result.split('\n')
            filtered_lines = []
            for line in lines:
                stripped_line = line.strip()
                if (
                    stripped_line.startswith(('def ', 'class ', 'function ', 'const ', 'let ', 'var ')) or
                    stripped_line.startswith(('"""', '#', '//', '/**', '*', '*/')) or
                    stripped_line.endswith((':', '(', '{', '}', ');')) or
                    re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', stripped_line) or
                    re.match(r'^\s*return\s+', stripped_line) or
                    re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\(', stripped_line)
                ):
                    filtered_lines.append(line)
            result = '\n'.join(filtered_lines)
            return result.strip()
        except Exception as e:
            print(f"Error generating code: {e}")
            return f"// Error generating code: {e}"