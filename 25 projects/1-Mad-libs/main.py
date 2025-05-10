import random
import time
import streamlit as st # type: ignore

def play_mad_libs():
    st.title("Welcome to the Ultimate Mad Libs Adventure! 🚀")
    st.markdown("***********************************************")  

    time.sleep(1)  # Kept your original pause
    st.subheader("🌟 Fill in the blanks with your words! 🌟")

    # Converted all inputs to Streamlit widgets
    adjective = st.text_input("Enter an adjective: ")
    adjective2 = st.text_input("Enter another adjective: ")
    animal = st.text_input("Enter an animal: ")
    verb = st.text_input("Enter a verb: ")
    place = st.text_input("Enter a place: ")
    profession = st.text_input("Enter a profession: ")
    character = st.text_input("Enter a fictional character: ")
    noun = st.text_input("Enter a random noun: ")

    # Your original story templates unchanged
    stories = [
        f"One day, a {adjective} {animal} decided to {verb} all the way to {place}. "
        "Everyone was amazed, and it became the talk of the town!",

        f"In a distant {place}, there was a {adjective} {profession} who always dreamed to {verb}. "
        f"One day, they found a magic {noun}, and their life changed forever!",

        f"Once upon a time, a {adjective} {character} discovered a secret {place}. "
        f"With the help of a {adjective2} {animal}, they {verb} their way to victory!"
    ]

    if st.button("Generate Story"):
        final_story = random.choice(stories)  # Your original random selection
        
        st.subheader("✨ Here is Your Mad Libs Story! ✨")
        st.write(final_story)  # Replaced print with st.write
        st.success("🎉 Hope you enjoyed it! 🎉")

        # Play again logic
        if st.button("Play Again"):
            st.experimental_rerun()

# Start the game
play_mad_libs()