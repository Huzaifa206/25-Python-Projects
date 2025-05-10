import time

print("🎮 I WILL GUESS YOUR NUMBER! 🎮") 

def choose_difficulty():
    print("\nChoose a Number Range:")
    print("1. Easy (1-10)")
    print("2. Medium (1-50)")
    print("3. Hard (1-100)")
    print("4. Custom Range")
    
    while True:
        choice = input("Enter 1, 2, 3, or 4: ").strip()
        if choice == "1":
            return 1, 10
        elif choice == "2":
            return 1, 50
        elif choice == "3":
            return 1, 100
        elif choice == "4":
            while True:
                try:
                    low = int(input("Enter the lowest number: "))
                    high = int(input("Enter the highest number: "))
                    if low < high:
                        return low, high
                    else:
                        print("\033[1;31mInvalid range! The lowest must be smaller than the highest.\033[0m")  # Red text
                except ValueError:
                    print("\033[1;31mPlease enter valid numbers.\033[0m")  # Red text
        else:
            print("\033[1;31mInvalid choice! Enter 1, 2, 3, or 4.\033[0m")  # Red text

def countdown():
    print("\nLet me think", end="")
    for _ in range(3):
        time.sleep(0.7)
        print(".", end="", flush=True)
    print("\n")

def computer_guesses():
    low, high = choose_difficulty()

    print("\nThink of a number between", low, "and", high, "but don't tell me!")
    input("\nPress ENTER when you're ready... ")

    countdown()

    attempts = 0
    while low <= high:
        attempts += 1
        guess = (low + high) // 2  # Smart Binary Search Guess
        print(f"\033[1;34mIs your number {guess}? (higher/lower/correct)\033[0m")  # Blue text
        
        while True:
            response = input("Type 'higher', 'lower', or 'correct': ").strip().lower()
            if response in ["higher", "lower", "correct"]:
                break
            print("\033[1;31mInvalid response! Please type 'higher', 'lower', or 'correct'.\033[0m")  # Red text
        
        if response == "higher":
            low = guess + 1
            print("\033[1;33mOhh, I need to go higher!\033[0m")  # Yellow text
        elif response == "lower":
            high = guess - 1
            print("\033[1;33mToo high? Alright, I'll go lower!\033[0m")  # Yellow text
        else:
            print(f"\033[1;32m🎉 YES! I guessed your number in {attempts} tries!\033[0m")  # Green text
            break

    if input("\nDo you want to play again? (yes/no): ").strip().lower() == "yes":
        computer_guesses()
    else:
        print("\nThanks for playing! Im a genius, right? 😎")

computer_guesses()
