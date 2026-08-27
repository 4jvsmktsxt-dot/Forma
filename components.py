import streamlit.components.v1 as components
import os
import streamlit as st

def render_model_viewer(file_path: str):
    """
    Renderöi Googlen model-viewer komponentin HTML:n kautta Streamlitiin,
    jotta .glb tiedosto pyörii suoraan selaimessa (interaktiivinen 3D-malli).
    """
    if not os.path.exists(file_path) and not file_path.startswith("http"):
        st.warning(f"⚠️ 3D-mallitiedostoa ei löytynyt polusta: {file_path}. Näytetään oletustila.")
        # Fallback jos tiedostoa ei löydy, ettei sivu kaadu
        return

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
        <style>
            model-viewer {{
                width: 100%;
                height: 500px;
                background-color: #f1f5f9;
                border-radius: 12px;
            }}
        </style>
    </head>
    <body>
        <model-viewer src="{file_path}" alt="3D Kohdemalli" auto-rotate camera-controls></model-viewer>
    </body>
    </html>
    """
    components.html(html_code, height=520)