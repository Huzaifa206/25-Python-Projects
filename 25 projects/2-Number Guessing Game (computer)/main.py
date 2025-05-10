import random
import time

print("************************")
print("🎮 GUESS THE NUMBER! 🎮")
print("************************")

def choose_difficulty():
    print("\nSelect Difficulty Level:")
    print("1. Easy (1-10)")
    print("2. Medium (1-50)")
    print("3. Hard (1-100)")
    
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            return 10
        elif choice == "2":
            return 50
        elif choice == "3":
            return 100
        else:
            print("\033[1;31mInvalid choice! Please enter 1, 2, or 3.\033[0m")  # Red text

def countdown():
    print("\nThinking of a number", end="")
    for _ in range(3):
        time.sleep(0.7)
        print(".", end="", flush=True)
    print("\n")

def play_game():
    max_number = choose_difficulty()
    secret_number = random.randint(1, max_number)
    
    countdown()

    attempts = 0
    while True:
        try:
            guess = int(input(f"Guess a number between 1 and {max_number}: "))
            attempts += 1
            
            if guess < 1 or guess > max_number:
                print("\033[1;31mOut of range! Try again.\033[0m")  # Red text
                continue
            
            if guess < secret_number:
                print("\033[1;33mToo low! Try again.\033[0m")  # Yellow text
            elif guess > secret_number:
                print("\033[1;33mToo high! Try again.\033[0m")  # Yellow text
            else:
                print(f"\033[1;32m🎉 Congratulations! You guessed it in {attempts} attempts!\033[0m")  # Green text
                break

        except ValueError:
            print("\033[1;31mInvalid input! Please enter a number.\033[0m")  # Red text

    if input("\nDo you want to play again? (yes/no): ").strip().lower() == "yes":
        play_game()
    else:
        print("\nThanks for playing! Goodbye! 👋")

play_game()