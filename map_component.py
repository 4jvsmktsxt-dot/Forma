import streamlit as st
import pandas as pd

def render_map_and_services(address: str):
    """
    Renderöi kartan ja alueen tärkeimmät palvelut (koulut, päiväkodit, ulkoilut, kaupat)
    kohteen ympäriltä, jotta Digitaalinen Kaksonen voi hyödyntää niitä myynnissä.
    """
    st.markdown("### 🗺️ Sijainti & Alueen Palvelut")
    st.caption(f"Kohteen osoite: **{address}** – Nämä tiedot ovat suoraan Digitaalisen Kaksosen tukena.")

    # Simuloitu koordinaatistodata (tuotannossa geokoodataan osoitteen perusteella)
    # Esimerkissä koordinaatit osuvat Helsinkiin
    map_data = pd.DataFrame({
        'lat': [60.1699],
        'lon': [24.9384]
    })
    
    # Näytetään interaktiivinen kartta
    st.map(map_data, zoom=13, use_container_width=True)

    st.markdown("---")
    
    # Alueen palvelukortit kahteen sarakkeeseen (Lapsiperheet vs. Aktiiviliikkujat)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏫 Lapsiperheet & Arki (esim. Matti)")
        st.write("- **Päiväkoti:** 350 m (Turvallinen reitti)")
        st.write("- **Alakoulu:** 750 m")
        st.write("- **Leikkipuisto:** 200 m")
        st.write("- **Lähikauppa:** 400 m")
    
    with col2:
        st.markdown("#### 🏃‍♂️ Aktiivisuus & Vapaa-aika (esim. Anna)")
        st.write("- **Ulkoilureitit / Kuntopolku:** 500 m")
        st.write("- **Kuntosali:** 600 m")
        st.write("- **Pyöräilyreitit:** Suora pääväylä keskustaan")
        st.write("- **Rauhallinen ympäristö:** Vähäinen liikennemelu")
