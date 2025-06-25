def add(x, y):
    """Addition operation"""
    return x + y

def subtract(x, y):
    """Subtraction operation"""
    return x - y

def multiply(x, y):
    """Multiplication operation"""
    return x * y

def divide(x, y):
    """Division operation"""
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y

def modulo(x, y):
    """Modulo operation"""
    if y == 0:
        raise ValueError("Cannot perform modulo with zero!")
    return x % y

def get_number(prompt):
    """Get a valid number from user input"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def get_operator():
    """Get a valid operator from user input"""
    valid_operators = ['+', '-', '*', '/', '%']
    
    while True:
        operator = input("Enter an operator (+, -, *, /, %): ").strip()
        if operator in valid_operators:
            return operator
        else:
            print("Invalid operator! Please enter one of: +, -, *, /, %")

def calculate(num1, num2, operator):
    """Perform the calculation based on the operator"""
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide,
        '%': modulo
    }
    
    return operations[operator](num1, num2)

def format_result(num1, num2, operator, result):
    """Format and return the calculation result as a string"""
    # Check if numbers are whole numbers for cleaner display
    num1_display = int(num1) if num1.is_integer() else num1
    num2_display = int(num2) if num2.is_integer() else num2
    
    # Format result based on whether it's a whole number
    if isinstance(result, float) and result.is_integer():
        result_display = int(result)
    else:
        result_display = round(result, 6)  # Round to 6 decimal places
    
    return f"{num1_display} {operator} {num2_display} = {result_display}"

def main():
    """Main calculator program"""
    print("=" * 40)
    print("         BASIC CALCULATOR")
    print("=" * 40)
    print("Supported operations: +, -, *, /, %")
    print("Enter 'quit' at any time to exit")
    print()
    
    while True:
        try:
            # Get first number
            print("Enter the first number (or 'quit' to exit):")
            user_input = input("First number: ").strip().lower()
            if user_input == 'quit':
                print("Thank you for using the calculator. Goodbye!")
                break
            
            try:
                num1 = float(user_input)
            except ValueError:
                print("Invalid input! Please enter a valid number.")
                continue
            
            # Get operator
            operator = get_operator()
            
            # Get second number
            num2 = get_number("Second number: ")
            
            # Perform calculation
            result = calculate(num1, num2, operator)
            
            # Display result
            print("\nResult:")
            print(format_result(num1, num2, operator, result))
            print("-" * 40)
            
            # Ask if user wants to continue
            continue_calc = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
            if continue_calc not in ['y', 'yes']:
                print("Thank you for using the calculator. Goodbye!")
                break
            
            print()  # Add spacing for next calculation
            
        except ValueError as e:
            print(f"Error: {e}")
            print("Please try again.")
            print()
            
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted. Goodbye!")
            break
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")
            print()

def demo_calculator():
    """Demonstrate calculator functionality without user input"""
    print("=== Calculator Demo ===")
    
    test_cases = [
        (10, 5, '+'),
        (15, 3, '-'),
        (7, 4, '*'),
        (20, 4, '/'),
        (17, 5, '%'),
        (10, 0, '/'),  # Division by zero test
    ]
    
    for num1, num2, op in test_cases:
        try:
            result = calculate(num1, num2, op)
            print(format_result(num1, num2, op, result))
        except ValueError as e:
            print(f"{num1} {op} {num2} = Error: {e}")
    
    print("=" * 30)

if __name__ == "__main__":
    # Ask user if they want to see demo or start calculator
    choice = input("Enter 'demo' to see examples or press Enter to start calculator: ").strip().lower()
    
    if choice == 'demo':
        demo_calculator()
        print()
        input("Press Enter to start the interactive calculator...")
        main()
    else:
        main()