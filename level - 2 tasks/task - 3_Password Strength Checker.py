import re
import string
from getpass import getpass

def check_password_strength(password):
    """
    Evaluate password strength based on multiple criteria
    Returns a dictionary with strength score and detailed feedback
    """
    score = 0
    feedback = []
    strength_details = {}
    
    # Check length
    length = len(password)
    if length >= 12:
        score += 25
        strength_details['length'] = "✅ Excellent length (12+ characters)"
    elif length >= 8:
        score += 15
        strength_details['length'] = "⚠️ Good length (8+ characters)"
    elif length >= 6:
        score += 5
        strength_details['length'] = "❌ Minimum length (6+ characters)"
        feedback.append("Consider using at least 8 characters")
    else:
        strength_details['length'] = "❌ Too short (less than 6 characters)"
        feedback.append("Password must be at least 6 characters long")
    
    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 10
        strength_details['lowercase'] = "✅ Contains lowercase letters"
    else:
        strength_details['lowercase'] = "❌ No lowercase letters"
        feedback.append("Add lowercase letters (a-z)")
    
    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 10
        strength_details['uppercase'] = "✅ Contains uppercase letters"
    else:
        strength_details['uppercase'] = "❌ No uppercase letters"
        feedback.append("Add uppercase letters (A-Z)")
    
    # Check for digits
    if re.search(r'\d', password):
        score += 10
        strength_details['digits'] = "✅ Contains numbers"
    else:
        strength_details['digits'] = "❌ No numbers"
        feedback.append("Add numbers (0-9)")
    
    # Check for special characters
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        score += 15
        strength_details['special'] = "✅ Contains special characters"
    else:
        strength_details['special'] = "❌ No special characters"
        feedback.append("Add special characters (!@#$%^&* etc.)")
    
    # Check for common patterns (bonus points for avoiding them)
    patterns_avoided = 0
    
    # No consecutive repeated characters
    if not re.search(r'(.)\1{2,}', password):
        patterns_avoided += 5
        strength_details['no_repeats'] = "✅ No excessive character repetition"
    else:
        strength_details['no_repeats'] = "⚠️ Contains repeated characters"
        feedback.append("Avoid repeating the same character multiple times")
    
    # No simple sequences
    sequences = ['123', '456', '789', 'abc', 'def', 'qwe', 'asd', 'zxc']
    has_sequence = any(seq in password.lower() for seq in sequences)
    if not has_sequence:
        patterns_avoided += 5
        strength_details['no_sequences'] = "✅ No common sequences"
    else:
        strength_details['no_sequences'] = "⚠️ Contains common sequences"
        feedback.append("Avoid simple sequences like '123' or 'abc'")
    
    # Check for common weak passwords
    common_weak = ['password', '123456', 'qwerty', 'admin', 'letmein']
    if password.lower() not in common_weak:
        patterns_avoided += 10
        strength_details['not_common'] = "✅ Not a common weak password"
    else:
        strength_details['not_common'] = "❌ This is a commonly used weak password"
        feedback.append("This password is too common and easily guessed")
    
    score += patterns_avoided
    
    # Determine overall strength
    if score >= 80:
        strength = "Very Strong"
        color = "🟢"
    elif score >= 60:
        strength = "Strong"
        color = "🟡"
    elif score >= 40:
        strength = "Moderate"
        color = "🟠"
    elif score >= 20:
        strength = "Weak"
        color = "🔴"
    else:
        strength = "Very Weak"
        color = "🔴"
    
    return {
        'score': score,
        'strength': strength,
        'color': color,
        'details': strength_details,
        'feedback': feedback
    }

def display_results(result):
    """Display the password strength results in a formatted way"""
    print("\n" + "="*60)
    print("🔒 PASSWORD STRENGTH ANALYSIS")
    print("="*60)
    
    # Overall score and strength
    print(f"{result['color']} Overall Strength: {result['strength']}")
    print(f"📊 Score: {result['score']}/100")
    print("\n" + "-"*60)
    print("📋 DETAILED BREAKDOWN:")
    print("-"*60)
    
    # Display each criterion
    for category, status in result['details'].items():
        print(f"  {status}")
    
    # Display feedback if any
    if result['feedback']:
        print("\n" + "-"*60)
        print("💡 SUGGESTIONS FOR IMPROVEMENT:")
        print("-"*60)
        for i, suggestion in enumerate(result['feedback'], 1):
            print(f"  {i}. {suggestion}")
    
    print("\n" + "="*60)

def generate_password_tips():
    """Display tips for creating strong passwords"""
    tips = [
        "Use at least 12 characters for maximum security",
        "Mix uppercase and lowercase letters",
        "Include numbers and special characters",
        "Avoid personal information (names, birthdays, etc.)",
        "Don't use common words or phrases",
        "Consider using passphrases with random words",
        "Use a unique password for each account",
        "Consider using a password manager"
    ]
    
    print("\n🛡️ TIPS FOR CREATING STRONG PASSWORDS:")
    print("-"*50)
    for i, tip in enumerate(tips, 1):
        print(f"  {i}. {tip}")

def main():
    """Main function to run the password strength checker"""
    print("🔐" + "="*58 + "🔐")
    print("           PASSWORD STRENGTH CHECKER")
    print("🔐" + "="*58 + "🔐")
    
    while True:
        print("\nOptions:")
        print("1. Check password strength")
        print("2. View password creation tips")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            # Get password input (hidden for security)
            print("\nEnter your password to check its strength:")
            print("(Your input will be hidden for security)")
            password = getpass("Password: ")
            
            if not password:
                print("❌ Please enter a password!")
                continue
            
            # Check password strength
            result = check_password_strength(password)
            display_results(result)
            
        elif choice == '2':
            generate_password_tips()
            
        elif choice == '3':
            print("\n🌟 Thanks for using the Password Strength Checker!")
            print("Stay secure! 🔒")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()