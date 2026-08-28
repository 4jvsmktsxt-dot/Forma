import streamlit as st
import pandas as pd
from database import init_db, add_property, get_properties, authenticate_user, add_user, get_all_users
from pricing import render_pricing_engine_ui

# Alustetaan tietokanta
init_db()

st.set_page_config(page_title="Forma - Digitaalinen Kaksonen & LKV", layout="wide")

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["user"] = None

    # Sivupalkki / Kirjautuminen
    st.sidebar.title("Kirjautuminen")
    
    if not st.session_state["authenticated"]:
        username = st.sidebar.text_input("Käyttäjätunnus")
        password = st.sidebar.text_input("Salasana", type="password")
        if st.sidebar.button("Kirjaudu sisään"):
            user = authenticate_user(username, password)
            if user:
                st.session_state["authenticated"] = True
                st.session_state["user"] = user
                st.rerun()
            else:
                st.sidebar.error("Virheellinen tunnus tai salasana")
        return

    user = st.session_state["user"]
    st.sidebar.success(f"Kirjautuneena: {user['name']} ({user['role']})")
    
    if st.sidebar.button("Kirjaudu ulos"):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.rerun()

    # Kohteen valinta tai uuden luonti
    st.sidebar.markdown("---")
    st.sidebar.subheader("Kohteen hallinta")
    
    properties_df = get_properties(user["name"])
    
    action = st.sidebar.radio("Toiminto", ["Valitse olemassa oleva kohde", "➕ Lisää uusi kohde"])
    
    if action == "➕ Lisää uusi kohde":
        st.markdown("## 🏠 Lisää uusi kohde (Asuntoilmoituksen tiedot)")
        st.markdown("Syötä kohteen perustiedot ennen median lataamista ja digitaalisen kakson luomista.")
        
        with st.form("new_property_form"):
            col1, col2 = st.columns(2)
            with col1:
                address = st.text_input("Osoite (esim. Länsitie 4 B 12)")
                pinta_ala = st.number_input("Pinta-ala (m²)", min_value=10.0, max_value=500.0, value=65.0)
                kunto = st.selectbox("Kunto", ["Erinomainen", "Hyvä", "Tyydyttävä", "Remontoitava"])
            with col2:
                asking_price = st.number_input("Hintapyyntö (€)", min_value=10000.0, max_value=10000000.0, value=250000.0, step=5000.0)
                makuuhuoneet = st.number_input("Makuuhuoneiden lukumäärä", min_value=0, max_value=10, value=2)
                huoneisto_tyyppi = st.text_input("Huoneistotyyppi (esim. 3h + k + s)", value="3h + k + s")
            
            submitted = st.form_submit_button("Tallenna kohde ja siirry mediaan")
            if submitted:
                if address:
                    # Tallennetaan tietokantaan omistajalle
                    add_property(address=address, asking_price=asking_price, property_type=huoneisto_tyyppi, owner=user["name"])
                    st.success(f"Kohde {address} lisätty onnistuneesti! Voit nyt ladata videot ja kuvat.")
                    st.rerun()
                else:
                    st.error("Osoite on pakollinen tieto.")
        return

    # Jos kohteita ei ole
    if properties_df.empty:
        st.warning("Ei vielä kohteita. Valitse vasemmalta '➕ Lisää uusi kohde'.")
        return

    selected_address = st.sidebar.selectbox("Valitse kohde", properties_df["address"].tolist())
    current_property = properties_df[properties_df["address"] == selected_address].iloc[0]
    
    asking_price = current_property["asking_price"]

    # Päänäyttö
    st.markdown(f"# 🌟 {user['name']} – Myynti- ja hallintapaneeli")
    st.markdown(f"Tehosta myyntiä digitaalisen kaksosen, videoiden ja reaaliaikaisten työkalujen avulla.")
    
    st.info(f"Aktiivinen kohde: **{selected_address}** (Pyydetty hinta: {asking_price:,.0f} €)".replace(",", " "))

    # Välilehdet
    tab1, tab2, tab3, tab4 = st.tabs(["🎥 Videot & Media (Aloita tästä)", "🗺️ Digitaalinen Kaksonen & Kartta", "📊 Analytiikka & Kyselyt", "💰 Hinnoittelu & Remonttilaskuri"])

    with tab1:
        st.markdown("### 📥 Rataa ja lataa videot / mediakuvat kohteelle")
        st.markdown(f"Lataa kohteen **{selected_address}** esittelyvideot ja panoraamakuvat.")
        uploaded_files = st.file_uploader("Valitse videot (mp4, mov) tai panoraamakuvat (jpg, png)", accept_multiple_files=True, type=["mp4", "mov", "jpg", "png"])
        if uploaded_files:
            st.success(f"Ladattu {len(uploaded_files)} tiedostoa onnistuneesti kohteelle {selected_address}!")

    with tab2:
        st.markdown("### 🗺️ Sijainti & Alueen Palvelut")
        st.markdown(f"Kohteen osoite: {selected_address} – Nämä tiedot ovat suoraan Digitaalisen Kaksosen tukena.")
        
        # Simuloitu karttanäkymä tai data
        map_data = pd.DataFrame({'lat': [60.1699], 'lon': [24.9384]})
        st.map(map_data, zoom=13)

        st.markdown("---")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("#### 👨‍👩‍👦 Lapsiperheet & Arki (esim. Matti)")
            st.markdown("- **Päiväkoti:** 350 m (Turvallinen reitti)")
            st.markdown("- **Alakoulu:** 750 m")
            st.markdown("- **Leikkipuisto:** 200 m")
            st.markdown("- **Lähikauppa:** 400 m")
        with col_m2:
            st.markdown("#### 🏃 Aktiivisuus & Vapaa-aika (esim. Anna)")
            st.markdown("- **Ulkoilureitit / Kuntopolku:** 500 m")
            st.markdown("- **Kuntosali:** 600 m")
            st.markdown("- **Pyöräilyreitit:** Suora pääväylä keskustaan")
            st.markdown("- **Rauhallinen ympäristö:** Vähäinen liikennemelu")

    with tab3:
        st.markdown("### 📊 Ostajapoolin palaute & analytiikka")
        st.markdown("Seuraa reaaliaikaisesti kiinnostusta ja digitaalisen kaksosen katselumääriä.")
        st.metric(label="Digitaalisen kaksosen interaktiot", value="42 kpl", delta="+12 tällä viikolla")

    with tab4:
        render_pricing_engine_ui(asking_price)

if __name__ == "__main__":
    main()
