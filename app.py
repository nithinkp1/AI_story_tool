import streamlit as st
from utils import generate_story, text_to_speech

# Set page config
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Hide Streamlit UI elements
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# App title
st.markdown("<h1 style='text-align: center; color: #6C63FF;'>✨ AI Story Generator ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Craft your own tale with AI magic — choose your mood and genre, then let the story unfold!</p>", unsafe_allow_html=True)

# Sidebar - Story Settings
st.sidebar.header("🛠️ Story Settings")
genre = st.sidebar.selectbox("Genre", ["Fantasy", "Sci-Fi", "Mystery", "Adventure"])
tone = st.sidebar.selectbox("Tone", ["Exciting", "Dramatic", "Humorous", "Dark"])
length = st.sidebar.slider("Story Length (Words)", 100, 500, 200, step=50)

# Prompt Input
st.markdown("### ✍️ Enter Your Story Prompt")
story_prompt = st.text_area("Start your story here...")

# Generate Button
if st.button("🚀 Generate Story"):
    if story_prompt.strip():
        with st.spinner("Generating your story..."):
            story = generate_story(story_prompt, genre, tone, length)

        if story.lower().startswith("error"):
            st.error(story)
        else:
            # Remove instruction prefix if it exists
            if story.lower().startswith("write a"):
                story = story.split(". ", 1)[-1].strip()

            st.success("Story generated successfully!")
            st.markdown("### 📚 Here's your story:")
            st.write(story)

            with st.spinner("Converting to narration..."):
                audio_file = text_to_speech(story)
                if audio_file:
                    st.markdown("### 🔊 Listen to your story:")
                    st.audio(audio_file, format="audio/mp3")
    else:
        st.warning("Please enter a prompt to generate your story.")

# Footer
st.markdown("---")
st.markdown("<small style='text-align:center;'>Created using Falcon-7B, Coqui TTS, and Streamlit</small>", unsafe_allow_html=True)
