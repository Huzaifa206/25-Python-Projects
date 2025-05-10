import streamlit as st
import random
import string

def generate_password(length, custom_chars):
    # Default chars plus any custom characters user wants to include
    chars = string.ascii_letters + string.digits + string.punctuation
    if custom_chars:
        chars += custom_chars
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    st.title("Password Generator with Custom Characters")
    num_passwords = st.number_input("Number of passwords to generate", min_value=1, max_value=20, value=5)
    length = st.number_input("Length of each password", min_value=6, max_value=50, value=12)
    custom_chars = st.text_input("Add your own characters to include (optional)")

    if st.button("Generate Passwords"):
        if len(custom_chars) > 0:
            st.write(f"Including custom characters: {custom_chars}")
        for i in range(num_passwords):
            pwd = generate_password(length, custom_chars)
            st.code(pwd)

if __name__ == "__main__":
    main()