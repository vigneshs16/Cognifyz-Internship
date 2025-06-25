import re

def is_palindrome_simple(s):
    """
    Basic palindrome checker - case sensitive, spaces matter.
    
    Args:
        s (str): The string to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not isinstance(s, str):
        return False
    
    return s == s[::-1]

def is_palindrome_case_insensitive(s):
    """
    Case-insensitive palindrome checker.
    
    Args:
        s (str): The string to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not isinstance(s, str):
        return False
    
    s = s.lower()
    return s == s[::-1]

def is_palindrome_ignore_spaces(s):
    """
    Palindrome checker that ignores spaces and case.
    
    Args:
        s (str): The string to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not isinstance(s, str):
        return False
    
    # Remove spaces and convert to lowercase
    cleaned = s.replace(' ', '').lower()
    return cleaned == cleaned[::-1]

def is_palindrome_alphanumeric_only(s):
    """
    Advanced palindrome checker that only considers alphanumeric characters
    and ignores case, spaces, and punctuation.
    
    Args:
        s (str): The string to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not isinstance(s, str):
        return False
    
    # Keep only alphanumeric characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]

def is_palindrome_two_pointers(s):
    """
    Palindrome checker using two-pointer technique (more memory efficient).
    Only considers alphanumeric characters, ignores case and punctuation.
    
    Args:
        s (str): The string to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not isinstance(s, str):
        return False
    
    # Convert to lowercase for case-insensitive comparison
    s = s.lower()
    left = 0
    right = len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric characters from left
        while left < right and not s[left].isalnum():
            left += 1
        
        # Skip non-alphanumeric characters from right
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare characters
        if s[left] != s[right]:
            return False
        
        left += 1
        right -= 1
    
    return True

def is_palindrome_recursive(s, start=0, end=None):
    """
    Recursive palindrome checker.
    
    Args:
        s (str): The string to check
        start (int): Starting index
        end (int): Ending index
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not isinstance(s, str):
        return False
    
    if end is None:
        end = len(s) - 1
    
    # Base case: if pointers meet or cross
    if start >= end:
        return True
    
    # If characters don't match
    if s[start] != s[end]:
        return False
    
    # Recursive call with inner substring
    return is_palindrome_recursive(s, start + 1, end - 1)

# Main function with multiple checking options
def is_palindrome(s, ignore_case=True, ignore_punctuation=True):
    """
    Comprehensive palindrome checker with options.
    
    Args:
        s (str): The string to check
        ignore_case (bool): Whether to ignore case differences
        ignore_punctuation (bool): Whether to ignore spaces and punctuation
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    if not isinstance(s, str):
        return False
    
    if ignore_punctuation:
        return is_palindrome_alphanumeric_only(s)
    elif ignore_case:
        return is_palindrome_case_insensitive(s)
    else:
        return is_palindrome_simple(s)

def test_palindrome_checker():
    """Test the palindrome checker with various test cases"""
    test_cases = [
        # Simple palindromes
        ("madam", True),
        ("racecar", True),
        ("level", True),
        ("noon", True),
        ("radar", True),
        
        # Non-palindromes
        ("hello", False),
        ("world", False),
        ("python", False),
        
        # Case sensitivity tests
        ("Madam", True),   # Should be True with ignore_case
        ("RaceCar", True), # Should be True with ignore_case
        
        # Phrases with spaces
        ("A man a plan a canal Panama", True),
        ("race a car", False),
        ("Was it a car or a cat I saw", True),
        
        # With punctuation
        ("A man, a plan, a canal: Panama!", True),
        ("race a car", False),
        ("Madam, I'm Adam", True),
        ("Never odd or even", True),
        
        # Edge cases
        ("", True),        # Empty string
        ("a", True),       # Single character
        ("aa", True),      # Two same characters
        ("ab", False),     # Two different characters
        
        # Numbers
        ("12321", True),
        ("12345", False),
        ("1221", True),
    ]
    
    print("=== Palindrome Checker Test Results ===\n")
    
    print("Testing with default settings (ignore case and punctuation):")
    print("-" * 60)
    
    for text, expected in test_cases:
        result = is_palindrome(text)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status} | '{text}' -> {result} (expected: {expected})")
    
    print("\n" + "=" * 60)
    
    # Test different modes
    test_phrase = "A man, a plan, a canal: Panama!"
    print(f"\nTesting different modes with: '{test_phrase}'")
    print("-" * 60)
    print(f"Simple (case & punctuation sensitive): {is_palindrome_simple(test_phrase)}")
    print(f"Case insensitive only: {is_palindrome_case_insensitive(test_phrase)}")
    print(f"Ignore spaces only: {is_palindrome_ignore_spaces(test_phrase.replace(',', '').replace(':', '').replace('!', ''))}")
    print(f"Ignore case & punctuation: {is_palindrome_alphanumeric_only(test_phrase)}")
    print(f"Two-pointer method: {is_palindrome_two_pointers(test_phrase)}")
    print(f"Recursive method: {is_palindrome_recursive(test_phrase.lower().replace(' ', '').replace(',', '').replace(':', '').replace('!', ''))}")

def main():
    """Interactive palindrome checker"""
    print("=== Palindrome Checker ===")
    print("This program checks if a string is a palindrome.")
    print("By default, it ignores case and punctuation.\n")
    
    while True:
        text = input("Enter a string to check (or 'test' to run tests, 'quit' to exit): ").strip()
        
        if text.lower() == 'quit':
            print("Goodbye!")
            break
        elif text.lower() == 'test':
            test_palindrome_checker()
            continue
        elif not text:
            print("Please enter a non-empty string.")
            continue
        
        # Check with different methods
        result_default = is_palindrome(text)
        result_simple = is_palindrome_simple(text)
        
        print(f"\nResults for: '{text}'")
        print("-" * 40)
        print(f"Default (ignore case & punctuation): {'✓ YES' if result_default else '✗ NO'}")
        print(f"Strict (exact match): {'✓ YES' if result_simple else '✗ NO'}")
        
        if result_default:
            cleaned = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
            print(f"Cleaned version: '{cleaned}'")
        
        print()

if __name__ == "__main__":
    main()