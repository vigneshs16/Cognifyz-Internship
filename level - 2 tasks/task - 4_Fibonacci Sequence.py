import time

def fibonacci_iterative(n):
    """
    Generate Fibonacci sequence using iterative method (most efficient)
    Returns a list of the first n Fibonacci numbers
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        next_num = sequence[i-1] + sequence[i-2]
        sequence.append(next_num)
    
    return sequence

def fibonacci_recursive(n):
    """
    Generate single Fibonacci number using recursion (educational purpose)
    Note: This is inefficient for large numbers
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_recursive_sequence(n):
    """Generate Fibonacci sequence using recursive method"""
    if n <= 0:
        return []
    return [fibonacci_recursive(i) for i in range(n)]

def fibonacci_generator(n):
    """
    Generator function for Fibonacci sequence (memory efficient)
    """
    a, b = 0, 1
    count = 0
    while count < n:
        if count <= 1:
            yield count
        else:
            yield a
            a, b = b, a + b
        count += 1

def fibonacci_golden_ratio(n):
    """
    Generate Fibonacci numbers using golden ratio formula (Binet's formula)
    Note: Less accurate for very large numbers due to floating point precision
    """
    import math
    
    if n <= 0:
        return []
    
    golden_ratio = (1 + math.sqrt(5)) / 2
    sequence = []
    
    for i in range(n):
        fib_num = round((golden_ratio**i - (-golden_ratio)**(-i)) / math.sqrt(5))
        sequence.append(fib_num)
    
    return sequence

def display_sequence(sequence, method_name, execution_time=None):
    """Display the Fibonacci sequence in a formatted way"""
    print(f"\n🔢 Fibonacci Sequence ({method_name}):")
    print("-" * 50)
    
    # Display sequence in rows of 10
    for i in range(0, len(sequence), 10):
        row = sequence[i:i+10]
        formatted_row = [f"{num:>8}" for num in row]
        print("  " + " ".join(formatted_row))
    
    print(f"\n📊 Total terms: {len(sequence)}")
    if sequence:
        print(f"🔝 Largest term: {sequence[-1]:,}")
    if execution_time:
        print(f"⏱️ Execution time: {execution_time:.6f} seconds")

def get_user_input():
    """Get number of terms from user with validation"""
    while True:
        try:
            n = int(input("\nEnter the number of Fibonacci terms to generate: "))
            if n < 0:
                print("❌ Please enter a non-negative number!")
                continue
            elif n > 1000:
                confirm = input(f"⚠️ Generating {n} terms might take a while. Continue? (y/n): ")
                if confirm.lower() not in ['y', 'yes']:
                    continue
            return n
        except ValueError:
            print("❌ Please enter a valid integer!")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

def compare_methods(n):
    """Compare different Fibonacci generation methods"""
    if n <= 0:
        print("❌ Cannot compare with 0 or negative terms!")
        return
    
    print(f"\n🏃 PERFORMANCE COMPARISON ({n} terms):")
    print("=" * 60)
    
    methods = [
        ("Iterative", fibonacci_iterative),
        ("Generator", lambda x: list(fibonacci_generator(x))),
        ("Golden Ratio", fibonacci_golden_ratio)
    ]
    
    # Add recursive method only for small numbers (it's very slow)
    if n <= 35:
        methods.append(("Recursive", fibonacci_recursive_sequence))
    
    results = []
    for name, method in methods:
        start_time = time.time()
        sequence = method(n)
        end_time = time.time()
        execution_time = end_time - start_time
        results.append((name, execution_time, sequence))
        print(f"{name:>12}: {execution_time:.6f} seconds")
    
    # Find fastest method
    fastest = min(results, key=lambda x: x[1])
    print(f"\n🏆 Fastest method: {fastest[0]} ({fastest[1]:.6f} seconds)")
    
    return results[0][2]  # Return the sequence from the first method

def show_fibonacci_facts():
    """Display interesting facts about Fibonacci sequence"""
    facts = [
        "🌟 The Fibonacci sequence starts with 0 and 1",
        "➕ Each number is the sum of the two preceding numbers",
        "🏛️ Named after Leonardo Fibonacci (c. 1170 – c. 1250)",
        "🌻 Found frequently in nature (flower petals, pinecones, shells)",
        "📐 The ratio of consecutive Fibonacci numbers approaches the Golden Ratio (φ ≈ 1.618)",
        "🔄 Every 3rd number is even, every 4th is divisible by 3",
        "🔢 F(n) = F(n-1) + F(n-2) is the defining recurrence relation",
        "💰 Used in financial markets for technical analysis",
        "🖥️ Applied in computer algorithms and data structures"
    ]
    
    print("\n📚 INTERESTING FIBONACCI FACTS:")
    print("=" * 50)
    for fact in facts:
        print(f"  {fact}")

def analyze_sequence(sequence):
    """Provide analysis of the generated sequence"""
    if not sequence:
        return
    
    print(f"\n🔍 SEQUENCE ANALYSIS:")
    print("-" * 30)
    print(f"First term: {sequence[0]}")
    if len(sequence) > 1:
        print(f"Last term: {sequence[-1]:,}")
        print(f"Sum of all terms: {sum(sequence):,}")
        
        # Calculate ratios between consecutive terms
        if len(sequence) > 2:
            ratios = [sequence[i]/sequence[i-1] for i in range(2, len(sequence)) if sequence[i-1] != 0]
            if ratios:
                avg_ratio = sum(ratios) / len(ratios)
                print(f"Average ratio (approaching φ): {avg_ratio:.6f}")
                print(f"Golden ratio (φ): 1.618034")

def main():
    """Main function to run the Fibonacci generator"""
    print("🌀" + "=" * 58 + "🌀")
    print("           FIBONACCI SEQUENCE GENERATOR")
    print("🌀" + "=" * 58 + "🌀")
    
    while True:
        print("\n📋 MENU OPTIONS:")
        print("1. Generate Fibonacci sequence (iterative method)")
        print("2. Generate with performance comparison")
        print("3. View Fibonacci facts")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            n = get_user_input()
            if n is None:
                break
            
            start_time = time.time()
            sequence = fibonacci_iterative(n)
            end_time = time.time()
            
            display_sequence(sequence, "Iterative Method", end_time - start_time)
            analyze_sequence(sequence)
            
        elif choice == '2':
            n = get_user_input()
            if n is None:
                break
            
            sequence = compare_methods(n)
            if sequence:
                analyze_sequence(sequence)
                
        elif choice == '3':
            show_fibonacci_facts()
            
        elif choice == '4':
            print("\n🌟 Thanks for exploring the Fibonacci sequence!")
            print("Math is beautiful! ✨")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()