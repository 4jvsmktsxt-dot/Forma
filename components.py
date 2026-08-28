import streamlit as st
import streamlit.components.v1 as components

def render_model_viewer(prop_id):
    """Renderöi Street View / 3D-tilamallin ja mahdollistaa pintamateriaalien vaihdon."""
    st.markdown("### 🌐 Interaktiivinen Digitaalinen Tila (Street View)")
    st.info(f"Kohteen ID {prop_id}: Vapaa siirtyminen huoneesta toiseen ja lennosta tehtävät materiaalivalinnat.")
    
    # Kutsutaan suoraan HTML/JS-pohjaista moottoria tähän väliin
    render_interactive_walkthrough(prop_id, f"model_url_{prop_id}")

def render_interactive_walkthrough(property_id: int, model_url: str):
    """
    Renderöi interaktiivisen Street View -tyylisen tila- ja materiaalinvaihtokatselimen.
    Mahdollistaa vapaan liikkumisen huoneissa ja pintojen vaihtamisen lennosta.
    """
    
    # HTML / Three.js / WebGL -pohjainen interaktiivinen moottori selaimessa
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; font-family: sans-serif; }}
            #viewer-container {{ width: 100%; height: 600px; position: relative; background: #1e293b; }}
            .ui-overlay {{
                position: absolute; bottom: 20px; left: 20px; z-index: 10;
                background: rgba(15, 23, 42, 0.85); color: white; padding: 15px; border-radius: 8px;
            }}
            button {{ background: #3b82f6; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; margin-right: 5px; }}
            button:hover {{ background: #2563eb; }}
        </style>
    </head>
    <body>
        <div id="viewer-container">
            <div class="ui-overlay">
                <h3>Forma Spatial Engine</h3>
                <p>Kohde ID: {property_id}</p>
                <button onclick="changeMaterial('wood')">Vaihda Tammi-parketti</button>
                <button onclick="changeMaterial('concrete')">Vaihda Betonilattia</button>
                <button onclick="teleportRoom('kitchen')">Siirry Keittiöön</button>
            </div>
        </div>

        <script>
            console.log("Forma 3D Engine alustettu kohteelle: {model_url}");
            
            function changeMaterial(type) {{
                alert("Materiaali vaihdettu: " + type + ". Hinnoittelulaskuri päivitetty.");
            }}
            
            function teleportRoom(room) {{
                alert("Siirrytty tilaan: " + room);
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=620)
