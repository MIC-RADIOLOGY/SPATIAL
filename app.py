import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Gesture UI", layout="wide")
st.title("🖐️ Gesture Controlled Spatial UI")

html_path = Path("web/index.html")

if not html_path.exists():
    st.error("❌ ERROR: Missing web/index.html")
    st.write("Your folder structure must be:")
    st.write("""
    gesture-streamlit-ui/
      app.py
      requirements.txt
      web/
        index.html
        style.css
        app.js
        handtrack.js
        gestures.js
        ui.js
    """)
else:
    html_content = html_path.read_text()
    st.components.v1.html(html_content, height=800, scrolling=False)

