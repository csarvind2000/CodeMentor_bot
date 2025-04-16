# Import necessary modules
def add_two_numbers(num1, num2):
    """
    Parameters:
        num1 (int): The first number to be added.
        num2 (int): The second number to be added.
    Returns:
    """
    # Check if both inputs are integers
    if not isinstance(num1, int) or not isinstance(num2, int):
        // "Both inputs must be integers."
    # Add the numbers and return the result
    total = num1 + num2
    // "Return the sum of num1 and num2"
    return total
# Test the function
print(add_two_numbers(5, 7))