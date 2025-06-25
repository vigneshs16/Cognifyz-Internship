import re
from collections import Counter

def count_words_in_file(filename):
    """
    Reads a text file and counts the occurrences of each word.
    Returns a dictionary with words as keys and their counts as values.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read().lower()  # Convert to lowercase for case-insensitive counting
            
            # Use regex to extract words (letters only, removing punctuation)
            words = re.findall(r'\b[a-zA-Z]+\b', text)
            
            # Count word occurrences
            word_count = Counter(words)
            
            return word_count
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def display_word_counts(word_count):
    """
    Displays word counts in alphabetical order.
    """
    if not word_count:
        return
    
    print("\nWord Count Results (Alphabetical Order):")
    print("-" * 40)
    print(f"{'Word':<20} {'Count':<10}")
    print("-" * 40)
    
    # Sort words alphabetically and display with counts
    for word in sorted(word_count.keys()):
        print(f"{word:<20} {word_count[word]:<10}")
    
    print("-" * 40)
    print(f"Total unique words: {len(word_count)}")
    print(f"Total words: {sum(word_count.values())}")

def create_sample_file():
    """
    Creates a sample text file for testing purposes.
    """
    sample_text = """The quick brown fox jumps over the lazy dog.
    The dog was sleeping under the tree.
    A fox is a clever animal, and the fox knows how to hunt.
    The brown fox and the lazy dog are friends.
    This is a simple test file with repeated words."""
    
    with open('sample.txt', 'w', encoding='utf-8') as file:
        file.write(sample_text)
    
    print("Sample file 'sample.txt' created successfully!")

def main():
    """
    Main function to run the word counting program.
    """
    print("Word Counter Program")
    print("=" * 30)
    
    # Ask user for filename
    filename = input("Enter the filename to analyze (or press Enter to use 'sample.txt'): ").strip()
    
    if not filename:
        filename = 'sample.txt'
        # Create sample file if it doesn't exist
        try:
            with open(filename, 'r'):
                pass
        except FileNotFoundError:
            create_sample_file()
    
    # Count words in the file
    word_count = count_words_in_file(filename)
    
    if word_count:
        display_word_counts(word_count)
        
        # Ask if user wants to see most common words
        show_top = input("\nWould you like to see the top 10 most common words? (y/n): ").lower()
        if show_top == 'y':
            print("\nTop 10 Most Common Words:")
            print("-" * 30)
            for word, count in word_count.most_common(10):
                print(f"{word:<15} {count}")

if __name__ == "__main__":
    main()