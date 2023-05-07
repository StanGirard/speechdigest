import streamlit as st
from utils import generate_image_prompt, generate_image
import theme

st.set_page_config(**theme.meme_config)


title = """
    <h1 style="color:#4caf50; font-family:sans-serif;">🎨 Meme Generator with DALL-E and GPT-4 🎨</h1>
"""
st.markdown(title, unsafe_allow_html=True)

api_key = st.text_input("Enter your OpenAI API key:", type="password")

if api_key:
    st.write("Generate a meme by entering a topic or a description.")
    user_input = st.text_input("Enter a topic or description:")

    if st.button("Generate Meme"):
        st.markdown("Generating meme text...")
        prompt = generate_image_prompt(api_key, user_input)
        st.markdown(f"### Generated Text: {prompt}")

        st.markdown("Generating meme image using DALL-E...")
        image_url = generate_image(api_key, prompt)
        st.markdown(f"### Generated Image:")
        st.image(image_url)
else:
    st.error("Please enter a valid OpenAI API key.")