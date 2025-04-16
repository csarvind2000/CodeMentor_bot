CodeMentor: Agent-Driven Code Commenting and Generation
Overview
CodeMentor is a web-based tool that uses AI agents to automatically add detailed comments to Python and JavaScript code and generate new code based on user requests. It leverages large language models (LLMs) via Ollama and provides a user-friendly interface built with Gradio.

Comment Code: Upload a .py or .js file or paste code to add inline comments for every line (reStructuredText for Python, JSDoc for JavaScript).
Generate Code: Request Python or JavaScript code generation with detailed comments included.

Prerequisites

Python: Version 3.8 or higher.
Ollama: For running the LLaMA 3 model locally.
Operating System: Tested on Linux (Ubuntu 20.04+), but should work on macOS and Windows with adjustments.

Setup Instructions
1. Clone the Repository
git clone <repository-url>
cd code_comment_bot

2. Install Ollama
Follow these steps to install and run Ollama on Linux (adjust for other OS as needed):
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the LLaMA 3 model
ollama pull llama3

# Start the Ollama server
ollama serve

3. Install Dependencies
Create a virtual environment and install the required Python packages:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

4. Run the Application
python app.py


Open the provided Gradio URL (e.g., http://127.0.0.1:7860) in your browser.
The app has two tabs: "Comment Code" and "Generate Code".

Usage
Comment Code

Upload a File or Paste Code:
In the "Comment Code" tab, either upload a .py or .js file or paste your code in the "Or Paste Code" textbox.
Optionally specify a filename (e.g., script.py) and a custom prompt for commenting.


Add Comments:
Click the "Add Comments" button.
View the commented code in the "Commented Code" textbox and download the file (e.g., commented_script.py).



Example Input:
function greet(name) {
    return `Hello, ${name}!`;
}

Sample Output (commented_greet.js):
/**
 * Module for greeting users.
 */
/**
 * Greets a user by name.
 * @param {string} name - The name of the user.
 * @returns {string} A greeting message.
 */
function greet(name) {
    // Constructs and returns a greeting string using template literal
    return `Hello, ${name}!`;
}

Generate Code

Request Code:
In the "Generate Code" tab, enter a code request (e.g., "Write a Python function to sort a list").
Select the file type (Python or JavaScript).


Generate Code:
Click the "Generate Code" button.
View the generated code in the "Generated Code" textbox and download the file (e.g., generated_code.py).



Example Request: "Write a Python function to sort a list"
Sample Output (generated_code.py):
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
    # Creates a new sorted list using the sorted() function
    sorted_numbers = sorted(numbers)
    # Returns the sorted list
    return sorted_numbers

Troubleshooting

Ollama Not Running:
Ensure the Ollama server is running (ollama serve).
Check for port conflicts on 11434: lsof -i :11434 and kill conflicting processes if needed.


Gradio URL Not Accessible:
Verify the app is running and check for port conflicts on 7860.
Try accessing the app in a different browser or in incognito mode.


Dependencies Issues:
Ensure you're in the virtual environment (source venv/bin/activate).
Reinstall dependencies: pip install -r requirements.txt.



License
This project is licensed under the MIT License.
