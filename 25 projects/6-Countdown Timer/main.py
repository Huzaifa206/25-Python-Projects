import time
import os

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)  # Convert to MM:SS format
        timer_display = f"{mins:02}:{secs:02}"
        print(f"\r⏳ Time left: {timer_display}", end="")
        time.sleep(1)
        seconds -= 1
    
    print("\n⏰ Time's up! 🎉")
    
    # Beep sound (only for Windows)
    if os.name == "nt":
        for _ in range(3):
            os.system("echo \a")
            time.sleep(0.10)

def main():
    print("\n🎯 Countdown Timer 🎯")
    
    while True:
        user_input = input("\nEnter time (e.g., '30' for 30 sec, '2m' for 2 min): ").strip().lower()
        
        if user_input.endswith("m"):  # Convert minutes to seconds
            try:
                seconds = int(user_input[:-1]) * 60
            except ValueError:
                print("❌ Invalid input. Try again.")
                continue
        else:  # Assume direct seconds
            try:
                seconds = int(user_input)
            except ValueError:
                print("❌ Invalid input. Try again.")
                continue
        
        countdown_timer(seconds)
        
        again = input("\nDo you want to start another countdown? (yes/no): ").strip().lower()
        if again != "yes":
            print("\nGoodbye! 🎮🔥")
            break

main()
