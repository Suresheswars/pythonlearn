import streamlit as st

st.title("My First App")

name = st.text_input("Plese enter your name:")

if st.button("Submit"):
    st.write(f"Hello {name}!")

    # Chainlit