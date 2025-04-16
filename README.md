# CodeMentor: Agent-Driven Code Commenting and Generation
CodeMentor is a web-based tool that uses AI agents to automatically add detailed comments to Python and JavaScript code and generate new code based on user requests. It leverages large language models (LLMs) via Ollama and provides a user-friendly interface built with Gradio.

## 📋 Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
  - [Comment Code](#comment-code)
  - [Generate Code](#generate-code)
- [Example Inputs and Outputs](#example-inputs-and-outputs)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🧠 Overview
CodeMentor offers two main features:

- ✅ **Comment Code:** Add inline comments to every line of Python or JavaScript code using LLMs (reStructuredText for Python, JSDoc for JavaScript).
- 🚀 **Generate Code:** Generate Python or JavaScript code with descriptive inline comments based on user instructions.

Built using:
- 🧠 **Ollama** for local LLaMA 3 model inference
- 🌐 **Gradio** for a simple web-based UI

## ⚙️ Prerequisites
- **Python:** 3.8 or higher
- **Ollama:** Installed and running for LLaMA 3 model
- **Operating System:** Tested on Linux (Ubuntu 20.04+). Should also work on macOS and Windows with minor tweaks.

## 🛠️ Setup Instructions
### 1. Clone the Repository
```bash
git clone <repository-url>
cd code_comment_bot
```

### 2. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
ollama serve
```

### 3. Install Python Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

Open the Gradio URL (http://127.0.0.1:7860) in your browser.

## 💡 Usage
### 📝 Comment Code
1. Upload a `.py` or `.js` file, or paste code.
2. Optionally provide filename and a custom prompt.
3. Click **Add Comments** to annotate the code.
4. Download or view the commented output.

### 🧾 Generate Code
1. Enter a code request prompt.
2. Select Python or JavaScript.
3. Click **Generate Code**.
4. Download or view the generated code.

## 🧪 Example Inputs and Outputs
### Comment Code
**Input:**
```javascript
function greet(name) {
    return `Hello, ${name}!`;
}
```

**Output:**
```javascript
/**
 * Module for greeting users.
 */
/**
 * Greets a user by name.
 * @param {string} name - The name of the user.
 * @returns {string} A greeting message.
 */
function greet(name) {
    // Constructs and returns a greeting string using a template literal.
    return `Hello, ${name}!`;
}
```

### Generate Code
**Prompt:** Write a Python function to sort a list

**Output:**
```python
"""
Module for sorting lists.
"""

def sort_list(numbers: list) -> list:
    """
    Sorts a list of numbers in ascending order.

    :param numbers: List of numbers to sort.
    :type numbers: list
    :returns: Sorted list in ascending order.
    :rtype: list
    """
    # Create a new sorted list using the sorted() function.
    sorted_numbers = sorted(numbers)
    # Return the sorted list.
    return sorted_numbers
```

## 🛠️ Troubleshooting
- **Ollama Not Running:**
  ```bash
  ollama serve
  lsof -i :11434  # Check port
  ```
- **Gradio App Not Opening:** Try a different browser or incognito.
- **Dependency Issues:**
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## 📄 License
This project is licensed under the **MIT License**.

---
🌟 Built with love and LLaMA.
