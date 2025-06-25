def reverse_string(s):
    """
    Takes a string as input and returns the reverse of that string.
    
    Args:
        s (str): The input string to be reversed
        
    Returns:
        str: The reversed string
    """
    return s[::-1]

# Example usage
if __name__ == "__main__":
    # Test the function
    test_string = "hello"
    result = reverse_string(test_string)
    print(f"Input: '{test_string}'")
    print(f"Output: '{result}'")
    
    # Additional test cases
    test_cases = ["hello", "world", "Python", "12345", "racecar", ""]
    
    print("\nAdditional test cases:")
    for test in test_cases:
        reversed_str = reverse_string(test)
        print(f"'{test}' -> '{reversed_str}'")