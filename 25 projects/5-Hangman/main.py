import random

# Hangman ASCII Art Stages
HANGMAN_STAGES = [
    """
       ------
       |    |
       |    
       |    
       |    
       |    
      ---
    """,
    """
       ------
       |    |
       |    O
       |    
       |    
       |    
      ---
    """,
    """
       ------
       |    |
       |    O
       |    |
       |    
       |    
      ---
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |    
       |    
      ---
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |    
       |    
      ---
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / 
       |    
      ---
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |    
      ---
    """
]

WORD_LIST = [
    "apple", "banana", "computer", "programming", "python",
    "developer", "internet", "keyboard", "hangman", "challenge",
    "elephant", "giraffe", "airplane", "university", "telescope"
]

print("\n🎮 Welcome to Hangman! 🎮\n")

def get_word(difficulty):
    
    if difficulty == "easy":
        filtered_words = [word for word in WORD_LIST if len(word) <= 6]
    elif difficulty == "medium":
        filtered_words = [word for word in WORD_LIST if 6 < len(word) <= 8]
    else:  # Hard
        filtered_words = [word for word in WORD_LIST if len(word) > 8]

    # If no words match the difficulty, choose randomly from all words
    if not filtered_words:
        print("\033[1;33mWarning: No words matched the difficulty level. Choosing a random word instead.\033[0m")
        filtered_words = WORD_LIST

    return random.choice(filtered_words)

def choose_difficulty():
    print("\nSelect Difficulty:")
    print("1. Easy (Short words, more chances)")
    print("2. Medium (Medium-length words, normal chances)")
    print("3. Hard (Long words, fewer chances)")

    while True:
        choice = input("\nEnter difficulty level (1, 2, or 3): ").strip()
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        print("\033[1;31mInvalid choice! Please enter 1, 2, or 3.\033[0m")  # Red text

def play_hangman():
    difficulty = choose_difficulty()
    word = get_word(difficulty)
    guessed_letters = []
    attempts = 6
    hidden_word = ["_" for _ in word]

    while attempts > 0 and "_" in hidden_word:
        print("\n" + HANGMAN_STAGES[6 - attempts])  # Show Hangman Stage
        print("Word:", " ".join(hidden_word))
        print(f"Attempts left: {attempts}")
        print(f"Guessed letters: {', '.join(guessed_letters)}")

        guess = input("\nGuess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("\033[1;31mInvalid input! Enter a single letter.\033[0m")
            continue

        if guess in guessed_letters:
            print("\033[1;33mYou already guessed that letter!\033[0m")
            continue

        guessed_letters.append(guess)

        if guess in word:
            print("\033[1;32mCorrect! 🔥\033[0m")
            for i, letter in enumerate(word):
                if letter == guess:
                    hidden_word[i] = guess
        else:
            print("\033[1;31mWrong guess! 💀\033[0m")
            attempts -= 1

    # Game Over
    if "_" not in hidden_word:
        print("\033[1;32m🎉 CONGRATULATIONS! YOU SURVIVED! 🎉\033[0m")
    else:
        print("\n" + HANGMAN_STAGES[-1])  # Show full Hangman
        print(f"\033[1;31m💀 GAME OVER! The word was: {word.upper()} 💀\033[0m")

    if input("\nDo you want to play again? (yes/no): ").strip().lower() == "yes":
        play_hangman()
    else:
        print("\nThanks for playing! 🎮🔥")

play_hangman()

