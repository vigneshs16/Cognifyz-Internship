import re

def validate_email(email):
    """
    Validates whether a given string is a valid email address.
    
    Args:
        email (str): The email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    # Check if email is a string and not empty
    if not isinstance(email, str) or not email.strip():
        return False
    
    email = email.strip()
    
    # Basic format check: must contain exactly one @
    if email.count('@') != 1:
        return False
    
    # Split into local and domain parts
    local_part, domain_part = email.split('@')
    
    # Check if both parts exist
    if not local_part or not domain_part:
        return False
    
    # Validate local part (before @)
    if not validate_local_part(local_part):
        return False
    
    # Validate domain part (after @)
    if not validate_domain_part(domain_part):
        return False
    
    return True

def validate_local_part(local):
    """
    Validates the local part of an email (before @).
    
    Args:
        local (str): The local part to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Length check (1-64 characters)
    if len(local) == 0 or len(local) > 64:
        return False
    
    # Cannot start or end with a dot
    if local.startswith('.') or local.endswith('.'):
        return False
    
    # Cannot have consecutive dots
    if '..' in local:
        return False
    
    # Check allowed characters
    allowed_chars = re.compile(r'^[a-zA-Z0-9._+-]+$')
    if not allowed_chars.match(local):
        return False
    
    return True

def validate_domain_part(domain):
    """
    Validates the domain part of an email (after @).
    
    Args:
        domain (str): The domain part to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Length check (1-255 characters)
    if len(domain) == 0 or len(domain) > 255:
        return False
    
    # Must contain at least one dot for TLD
    if '.' not in domain:
        return False
    
    # Cannot start or end with a dot or hyphen
    if domain.startswith('.') or domain.endswith('.') or domain.startswith('-') or domain.endswith('-'):
        return False
    
    # Cannot have consecutive dots
    if '..' in domain:
        return False
    
    # Split domain into labels (parts separated by dots)
    labels = domain.split('.')
    
    # Each label must be valid
    for label in labels:
        if not validate_domain_label(label):
            return False
    
    # Last label (TLD) must be at least 2 characters and contain only letters
    if len(labels[-1]) < 2 or not labels[-1].isalpha():
        return False
    
    return True

def validate_domain_label(label):
    """
    Validates a single domain label.
    
    Args:
        label (str): The domain label to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Length check (1-63 characters)
    if len(label) == 0 or len(label) > 63:
        return False
    
    # Cannot start or end with hyphen
    if label.startswith('-') or label.endswith('-'):
        return False
    
    # Check allowed characters (letters, numbers, hyphens)
    allowed_chars = re.compile(r'^[a-zA-Z0-9-]+$')
    if not allowed_chars.match(label):
        return False
    
    return True

def validate_email_regex(email):
    """
    Alternative email validation using regex (more concise but less detailed error handling).
    
    Args:
        email (str): The email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    if not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

# Test function
def test_email_validator():
    """Test the email validator with various test cases"""
    test_cases = [
        # Valid emails
        ("user@example.com", True),
        ("test.email@domain.co.uk", True),
        ("user+tag@example.org", True),
        ("first.last@subdomain.example.com", True),
        ("user_name@example-domain.com", True),
        
        # Invalid emails
        ("", False),                           # Empty string
        ("invalid", False),                    # No @ symbol
        ("@example.com", False),               # No local part
        ("user@", False),                      # No domain part
        ("user@@example.com", False),          # Multiple @ symbols
        ("user@example", False),               # No TLD
        ("user@.example.com", False),          # Domain starts with dot
        ("user@example.com.", False),          # Domain ends with dot
        ("user@example..com", False),          # Consecutive dots in domain
        (".user@example.com", False),          # Local part starts with dot
        ("user.@example.com", False),          # Local part ends with dot
        ("us..er@example.com", False),         # Consecutive dots in local part
        ("user@ex ample.com", False),          # Space in domain
        ("user@example.c", False),             # TLD too short
    ]
    
    print("=== Email Validator Test Results ===\n")
    
    for email, expected in test_cases:
        result = validate_email(email)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status} | '{email}' -> {result} (expected: {expected})")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    # Interactive testing
    print("=== Email Validator ===")
    print("This program validates email addresses.")
    
    while True:
        email = input("\nEnter an email address to validate (or 'test' to run tests, 'quit' to exit): ").strip()
        
        if email.lower() == 'quit':
            print("Goodbye!")
            break
        elif email.lower() == 'test':
            test_email_validator()
        else:
            is_valid = validate_email(email)
            if is_valid:
                print(f"✓ '{email}' is a VALID email address.")
            else:
                print(f"✗ '{email}' is NOT a valid email address.")