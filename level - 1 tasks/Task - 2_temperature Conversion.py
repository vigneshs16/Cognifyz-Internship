def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9

def main():
    """Main program function"""
    print("=== Temperature Converter ===")
    print("This program converts temperatures between Celsius and Fahrenheit.")
    
    while True:
        try:
            # Get temperature value from user
            temp_value = float(input("\nEnter the temperature value: "))
            
            # Get unit from user
            print("\nSelect the unit of the temperature you entered:")
            print("1. Celsius (C)")
            print("2. Fahrenheit (F)")
            
            unit_choice = input("Enter your choice (1 or 2): ").strip()
            
            if unit_choice == "1" or unit_choice.lower() == "c":
                # Convert Celsius to Fahrenheit
                converted_temp = celsius_to_fahrenheit(temp_value)
                print(f"\n{temp_value}°C = {converted_temp:.2f}°F")
                
            elif unit_choice == "2" or unit_choice.lower() == "f":
                # Convert Fahrenheit to Celsius
                converted_temp = fahrenheit_to_celsius(temp_value)
                print(f"\n{temp_value}°F = {converted_temp:.2f}°C")
                
            else:
                print("Invalid choice! Please enter 1 or 2.")
                continue
            
            # Ask if user wants to continue
            again = input("\nDo you want to convert another temperature? (y/n): ").strip().lower()
            if again != 'y' and again != 'yes':
                print("Thank you for using the Temperature Converter!")
                break
                
        except ValueError:
            print("Invalid input! Please enter a valid number for temperature.")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break

if __name__ == "__main__":
    main()