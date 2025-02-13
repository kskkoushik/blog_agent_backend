import streamlit as st
import time
import random
from agent_sim import generate_custom_blog, generate_trending_blog

# Custom Styling
st.markdown(
    """
    <style>
        /* Background and text styling */
        body { background-color: #0f0f0f; color: white; }
        .stButton>button { 
            background-color: #ff4b4b; 
            color: white; 
            border-radius: 10px; 
            font-size: 18px;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar: API Key Input
st.sidebar.image("image.png", width=600)
st.sidebar.header("🔑 Enter OpenAI API Key")
api_key = st.sidebar.text_input("API Key", type="password")

if not api_key:
    st.sidebar.warning("⚠️ Please enter your API key to use the app.")
    st.stop()

# Title
st.title("✍️ AI Blog Generator")
st.markdown("#### 🚀 Generate AI-powered blogs with ease!")

# Main Options
option = st.radio(
    "Choose an option:", 
    ["📝 Generate Custom Blog", "🔥 Generate Trending Blog"],
    horizontal=True
)

st.divider()  # Adds a visual separator

if option == "📝 Generate Custom Blog":
    st.subheader("Custom Blog Settings")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("🖊️ Blog Topic")
    with col2:
        tone = st.selectbox("🎭 Select Tone", ["Professional", "Human Expert", "AI Tone"])

    size = st.radio("📏 Select Size", ["Medium", "Long"], horizontal=True)

    # Generate button
    generate_btn = st.button("🚀 Generate Blog", disabled=not(topic and tone and size))

    if generate_btn:
        with st.spinner("📝 Generating Blog... Please wait."):
            blog_url = generate_custom_blog(topic, tone, size, api_key)
            st.success("✅ Blog Generated Successfully!")
            st.toast("🎉 Blog is ready!")
            st.write(f"📖 [Read the blog here]({blog_url})")
            st.balloons()

            # Share & Copy
            st.text_input("🔗 Copy URL", blog_url)
            st.markdown(f"[🔗 Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url={blog_url})")
            st.markdown(f"[🐦 Share on Twitter](https://twitter.com/intent/tweet?url={blog_url}&text=Check%20out%20this%20AI-generated%20blog!)")

elif option == "🔥 Generate Trending Blog":
    st.subheader("Trending Blog Generator")

    trend_btn = st.button("🌍 Get Trending Blog")

    if trend_btn:
        with st.spinner("📡 Fetching trending blog..."):
            trend_url = generate_trending_blog(api_key)
            st.success("🚀 Trending Blog Ready!")
            st.toast("🔥 Hot Content Incoming!")
            st.write(f"📢 [Read the trending blog]({trend_url})")
            st.balloons()

            # Share & Copy
            st.text_input("🔗 Copy URL", trend_url)
            st.markdown(f"[🔗 Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url={trend_url})")
            st.markdown(f"[🐦 Share on Twitter](https://twitter.com/intent/tweet?url={trend_url}&text=Trending%20AI-generated%20blog!)")
