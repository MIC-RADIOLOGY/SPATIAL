import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Gesture UI", layout="wide")
st.title("🖐️ Gesture Controlled Spatial UI")

html_path = Path("web/index.html")

st.write("Checking file path:", html_path.resolve())

if not html_path.exists():
    st.error("❌ ERROR: Missing web/index.html")
    st.write("Current working directory:", Path.cwd())
    st.write("Directory contents:", list(Path.cwd().iterdir()))
else:
    html_content = html_path.read_text()
    st.components.v1.html(html_content, height=800, scrolling=False)
