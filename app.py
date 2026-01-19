import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Gesture Controlled Spatial UI",
    layout="wide"
)

st.title("🖐️ Gesture Controlled Spatial UI")

# Read the HTML file
html_path = Path("web/index.html")
html_content = html_path.read_text()

# Display the HTML inside Streamlit
st.components.v1.html(
    html_content,
    height=800,
    scrolling=False
)
