import random

def get_range():
    """Get the number range from the user"""
    while True:
        try:
            print("🎯 Welcome to the Number Guesser Game!")
            print("First, let's set up your game range.")
            print("-" * 40)
            
            min_num = int(input("Enter the minimum number: "))
            max_num = int(input("Enter the maximum number: "))
            
            if min_num >= max_num:
                print("❌ Maximum must be greater than minimum! Try again.\n")
                continue
                
            return min_num, max_num
            
        except ValueError:
            print("❌ Please enter valid numbers!\n")

def guessing_game():
    # Get the range from user
    min_num, max_num = get_range()
    
    # Generate random number in the specified range
    secret_number = random.randint(min_num, max_num)
    attempts = 0
    
    print(f"\n✨ Great! I'm thinking of a number between {min_num} and {max_num}.")
    print("Can you guess what it is?")
    print("-" * 40)
    
    while True:
        try:
            # Get user's guess
            guess = int(input(f"Enter your guess ({min_num}-{max_num}): "))
            attempts += 1
            
            # Check if guess is in valid range
            if guess < min_num or guess > max_num:
                print(f"⚠️  Please guess a number between {min_num} and {max_num}!")
                continue
            
            # Check if guess is correct
            if guess == secret_number:
                print(f"🎉 Congratulations! You guessed it!")
                print(f"The number was {secret_number}")
                if attempts == 1:
                    print("🏆 Amazing! You got it in just 1 attempt!")
                else:
                    print(f"It took you {attempts} attempts.")
                break
            elif guess < secret_number:
                print("📈 Too low! Try a higher number.")
            else:
                print("📉 Too high! Try a lower number.")
                
            # Give encouragement based on attempts
            if attempts == 5:
                print("💪 Keep going! You're getting closer!")
            elif attempts == 10:
                print("🤔 Hmm, this is tricky! Don't give up!")
                
        except ValueError:
            print("❌ Please enter a valid number!")
        except KeyboardInterrupt:
            print("\n👋 Thanks for playing! Goodbye!")
            break

def play_again():
    """Ask if the user wants to play again"""
    while True:
        choice = input("\nWould you like to play again? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def show_difficulty_stats(min_num, max_num):
    """Show some stats about the difficulty"""
    range_size = max_num - min_num + 1
    if range_size <= 10:
        difficulty = "Very Easy"
    elif range_size <= 50:
        difficulty = "Easy"
    elif range_size <= 100:
        difficulty = "Medium"
    elif range_size <= 500:
        difficulty = "Hard"
    else:
        difficulty = "Very Hard"
    
    print(f"📊 Range size: {range_size} numbers")
    print(f"🎯 Difficulty: {difficulty}")

# Main game loop
if __name__ == "__main__":
    print("🎮" + "="*50 + "🎮")
    print("           CUSTOMIZABLE NUMBER GUESSER")
    print("🎮" + "="*50 + "🎮")
    
    while True:
        guessing_game()
        if not play_again():
            print("\n🌟 Thanks for playing! Have a great day! 🌟")
            break
        print("\n" + "="*52)