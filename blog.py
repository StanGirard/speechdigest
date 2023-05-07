import streamlit as st
from utils import transcribe_audio, summarize_transcript, generate_image_prompt, generate_image, call_gpt, call_gpt_streaming, generate_images
import time
import openai
import theme

# Streamlit App

st.set_page_config(**theme.blog_config)

st.title("Article Genius")


st.markdown("Harness the power of AI to discover relevant resources, craft captivating introductions, subheadings, and conclusions, and generate eye-catching visuals for your blog.")

api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

models = ["gpt-3.5-turbo", "gpt-4"]
model = st.sidebar.selectbox("Select a model:", models)

st.sidebar.header("Article Information")
article_title = st.sidebar.text_area("Enter the article title:")

st.sidebar.header("Steps")
step = st.sidebar.radio(
    "Choose a step:",
    ("Idea Generation", "Introduction", "Headings Creation", "Outro", "Excerpt", "Image Generation", "Summary")
)


@st.cache_resource
def get_state():
    state = {
        "topic": "",
        "introduction": "",
        "subheadings": "",
        "outro": "",
        "excerpt": "",
        "ideas": "",
        "ideas_result": "",
        "image": "",
        "images": [],
    }
    return state

state = get_state()
state["topic"] = article_title

if st.sidebar.button("Reset"):
     st.cache_resource.clear()
    

if step == "Idea Generation":
    st.header("Idea Generation")
    state["ideas"] = st.text_input("Enter a topic or list of keywords:", value=state["ideas"])
    st.write(state["ideas_result"])
    if st.button("Generate Ideas"):
        st.empty()
        with st.spinner("Generating ideas..."):
            prompt = f"Generate a list of 3 blog post ideas about :{state['ideas']}. It should have the title and a short description and combine if possible the keywords entered"
            ideas = call_gpt_streaming(api_key,prompt, model)
            state["ideas_result"] = ideas

elif step == "Introduction":
    st.header("Introduction")
    st.write(state["introduction"])
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if st.button("Generate Introduction"):
        st.empty()
        with st.spinner("Generating introduction..."):
            prompt = f"Write an engaging introduction for a blog post titled '{article_title}':"
            state["introduction"] = call_gpt_streaming(api_key,prompt, model)

elif step == "Headings Creation":
    st.header("Headings Creation")
    st.write(state["subheadings"])
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if st.button("Generate Headings"):
        st.empty()
        with st.spinner("Generating headings..."):
            prompt = f"Generate up to 6 subheadings for a blog post titled :'{article_title}'. It should have the title and a short description of each subheading and each subheading should be separated by a new line"
            subheadings = call_gpt_streaming(api_key,prompt, model)
            state["subheadings"] = subheadings

elif step == "Outro":
    st.header("Outro")
    st.write(state["outro"])
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if st.button("Generate Outro"):
        st.empty()
        with st.spinner("Generating outro..."):
            prompt = f"Write a conclusion for a blog post titled '{article_title}':"
            state["outro"] = call_gpt_streaming(api_key,prompt, model)

elif step == "Excerpt":
    st.header("Excerpt")
    st.write(state["excerpt"])
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if st.button("Generate Excerpt"):
        st.empty()
        with st.spinner("Generating excerpt..."):
            prompt = f"Write a brief, attention-grabbing excerpt or meta description for a blog post about '{article_title}':"
            state["excerpt"] = call_gpt_streaming(api_key,prompt, model)

elif step == "Image Generation":
    st.header("Image Generation")
    image_url = state["images"]
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if image_url:
        for image in image_url:
            st.image(image)
    if st.button("Generate Image"):
        image_dalle = ""
        st.empty()
        with st.spinner("Generating Prompt for Image..."):
                image_prompt = f"You are an expert Prompt Engineer, you role is to create a prompt that will be used by Dall-E to generate an image. Here are a few example of dall-e prompts: - 3D render of a cute tropical fish in an aquarium on a dark blue background, digital art; - An expressive oil painting of a basketball player dunking, depicted as an explosion of a nebula;A photo of a teddy bear on a skateboard in Times Square; - A photograph of a sunflower with sunglasses on in the middle of the flower in a field on a bright sunny day; - A 3D render of a rainbow colored hot air balloon flying above a reflective lake; I want you to generate a prompt that takes the essence of this article and generates an image that is relevant to the article. You MUST not use technical terms and everything should be explained with simple words that a 12 years old could understand and nothing related to the topic of the article.The image will used for an article and needs to be detailed and professional. The article is about '{state['topic']}'."
                image_dalle = call_gpt_streaming(api_key,image_prompt, model)
        with st.spinner("Generating image..."):
            image_url = generate_images(api_key, image_dalle)
            # response['data'][0]['url']
            state["images"] = []
            for image in image_url:
                state["images"].append(image['url'])
                st.image(image['url'])

elif step == "Summary":
    st.header("Summary")
    if state["topic"] != "":
        st.write(f"### Article Title:\n{state['topic']}\n")
    if state["introduction"] != "":
        st.write(f"### Introduction:\n{state['introduction']}\n")
    if state["subheadings"] != "":
        st.write(f"### Headings :\n{state['subheadings']}\n")
    if state["outro"] != "":
        st.write(f"### Outro:\n{state['outro']}\n")
    if state["excerpt"] != "":
        st.write(f"### Excerpt:\n{state['excerpt']}\n")
    if state["images"]:
        st.write("### Generated Images:")
        for image in state["images"]:
            st.image(image)


st.markdown(
    """
    ---
    ### Source code and contact information
    - The source code for this app can be found on GitHub: [SpeechDigest](https://github.com/StanGirard/speechdigest)
    - If you have any questions or comments, feel free to reach out to me on Twitter: [@_StanGirard](https://twitter.com/_StanGirard)
    """
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        [![Tweet](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FStanGirard%2Fspeechdigest)](https://twitter.com/intent/tweet?url=https://github.com/StanGirard/speechdigest&text=Check%20out%20this%20awesome%20Speech%20Digest%20app%20built%20with%20Streamlit!%20%23speechdigest%20%23streamlit)
        """
    )

with col2:
    st.markdown(
        """
        [![GitHub Stars](https://img.shields.io/github/stars/StanGirard/speechdigest?style=social)](https://github.com/StanGirard/speechdigest/stargazers)
        """
    )