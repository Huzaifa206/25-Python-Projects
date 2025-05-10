import random
import time

print("🎮 ROCK, PAPER, SCISSORS! 🎮")  # Cyan color

def get_user_choice():
    choices = ["rock", "paper", "scissors"]
    while True:
        user_input = input("\nChoose Rock, Paper, or Scissors: ").strip().lower()
        if user_input in choices:
            return user_input
        print("\033[1;31mInvalid choice! Please enter Rock, Paper, or Scissors.\033[0m")  # Red text

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(user, computer):
    if user == computer:
        return "tie"
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        return "user"
    else:
        return "computer"

def display_result(user, computer, winner):
    print(f"\n\033[1;34mYou chose: {user.capitalize()}\033[0m")  # Blue text
    time.sleep(0.5)
    print(f"\033[1;35mComputer chose: {computer.capitalize()}\033[0m")  # Purple text
    time.sleep(0.5)

    if winner == "tie":
        print("\033[1;33mIt's a tie! 😐\033[0m")  # Yellow text
    elif winner == "user":
        print("\033[1;32mYou win! 🎉🔥\033[0m")  # Green text
    else:
        print("\033[1;31mComputer wins! 🤖💀\033[0m")  # Red text

def play_best_of_three():
    user_score = 0
    computer_score = 0

    while user_score < 2 and computer_score < 2:
        user = get_user_choice()
        computer = get_computer_choice()
        winner = determine_winner(user, computer)
        display_result(user, computer, winner)

        if winner == "user":
            user_score += 1
        elif winner == "computer":
            computer_score += 1

        print(f"\nScore - You: {user_score} | Computer: {computer_score}")

    if user_score > computer_score:
        print("\033[1;32m🎉 YOU WIN THE BEST OF 3! 🎉\033[0m")
    else:
        print("\033[1;31m💀 COMPUTER WINS THE BEST OF 3! 💀\033[0m")

def play_infinite_mode():
    while True:
        user = get_user_choice()
        computer = get_computer_choice()
        winner = determine_winner(user, computer)
        display_result(user, computer, winner)

        if input("\nPlay again? (yes/no): ").strip().lower() != "yes":
            break

def start_game():
    print("\nGame Modes:")
    print("1. Best of 3")
    print("2. Infinite Mode")

    while True:
        mode = input("\nChoose mode (1 or 2): ").strip()
        if mode == "1":
            play_best_of_three()
            break
        elif mode == "2":
            play_infinite_mode()
            break
        else:
            print("\033[1;31mInvalid choice! Enter 1 or 2.\033[0m")  # Red text

    print("\nThanks for playing! 🎮🔥")

start_game()
