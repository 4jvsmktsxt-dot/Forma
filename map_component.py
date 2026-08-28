import streamlit as st
import pandas as pd
from database import init_db, add_property, get_properties, authenticate_user, add_user, get_all_users
from pricing import render_pricing_engine_ui
from map_component import render_map_and_services

# Alustetaan tietokanta
init_db()

st.set_page_config(page_title="Forma - Digitaalinen Kaksonen & LKV", layout="wide")

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["user"] = None

    if "nav_action" not in st.session_state:
        st.session_state["nav_action"] = "Valitse olemassa oleva kohde"

    if "active_property" not in st.session_state:
        st.session_state["active_property"] = None

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
        st.session_state["nav_action"] = "Valitse olemassa oleva kohde"
        st.rerun()

    # Kohteen valinta tai uuden luonti
    st.sidebar.markdown("---")
    st.sidebar.subheader("Kohteen hallinta")
    
    properties_df = get_properties(user["name"])
    
    action_options = ["Valitse olemassa oleva kohde", "➕ Lisää uusi kohde"]
    current_index = 0 if st.session_state["nav_action"] == "Valitse olemassa oleva kohde" else 1
    
    action = st.sidebar.radio("Toiminto", action_options, index=current_index)
    st.session_state["nav_action"] = action
    
    if action == "➕ Lisää uusi kohde":
        st.markdown("## 🏠 Lisää uusi kohde (Asuntoilmoituksen tiedot)")
        st.markdown("Syötä kohteen perustiedot ennen median lataamista ja digitaalisen kakson luomista.")
        
        col1, col2 = st.columns(2)
        with col1:
            katuosoite = st.text_input("Katuosoite (esim. Länsitie 4 B 12)")
            postinumero = st.text_input("Postinumero (esim. 00100)")
            kaupunki = st.text_input("Kaupunki (esim. Helsinki)")
            pinta_ala = st.number_input("Pinta-ala (m²)", min_value=10.0, max_value=500.0, value=65.0)
            kunto = st.selectbox("Kunto", ["Erinomainen", "Hyvä", "Tyydyttävä", "Remontoitava"])
        with col2:
            asking_price = st.number_input("Hintapyyntö (€)", min_value=10000.0, max_value=10000000.0, value=250000.0, step=5000.0)
            makuuhuoneet = st.number_input("Makuuhuoneiden lukumäärä", min_value=0, max_value=10, value=2)
            huoneisto_tyyppi = st.text_input("Huoneistotyyppi (esim. 3h + k + s)", value="3h + k + s")
        
        if st.button("Tallenna kohde ja siirry mediaan"):
            if katuosoite and postinumero and kaupunki:
                koko_osoite = f"{katuosoite}, {postinumero} {kaupunki}"
                
                existing_addresses = [str(addr).strip().lower() for addr in properties_df["address"].tolist()] if not properties_df.empty else []
                clean_address = koko_osoite.strip().lower()
                
                if clean_address in existing_addresses:
                    st.error(f"Kohde osoitteella '{koko_osoite}' on jo olemassa! Valitse se olemassa olevista kohteista.")
                else:
                    add_property(address=koko_osoite, asking_price=asking_price, property_type=huoneisto_tyyppi, owner=user["name"])
                    st.session_state["nav_action"] = "Valitse olemassa oleva kohde"
                    st.session_state["active_property"] = koko_osoite
                    st.success(f"Kohde {koko_osoite} lisätty onnistuneesti! Siirrytään mediaan...")
                    st.rerun()
            else:
                st.error("Katuosoite, postinumero ja kaupunki ovat pakollisia tietoja.")
        return

    # Jos kohteita ei ole
    if properties_df.empty:
        st.warning("Ei vielä kohteita. Valitse vasemmalta '➕ Lisää uusi kohde'.")
        return

    addresses = properties_df["address"].tolist()
    
    default_index = 0
    if st.session_state["active_property"] in addresses:
        default_index = addresses.index(st.session_state["active_property"])

    selected_address = st.sidebar.selectbox("Valitse kohde", addresses, index=default_index)
    st.session_state["active_property"] = selected_address
    
    current_property = properties_df[properties_df["address"] == selected_address].iloc[0]
    asking_price = current_property["asking_price"]

    # Päänäyttö
    st.markdown(f"# 🌟 {user['name']} – Myynti- ja hallintapaneeli")
    st.markdown("Tehosta myyntiä digitaalisen kaksosen, videoiden ja reaaliaikaisten työkalujen avulla.")
    
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
        # Kutsutaan map_component-tiedoston funktiota suoraan valitulla osoitteella!
        render_map_and_services(selected_address)

    with tab3:
        st.markdown("### 📊 Ostajapoolin palaute & analytiikka")
        st.markdown("Seuraa reaaliaikaisesti kiinnostusta ja digitaalisen kaksosen katselumääriä.")
        st.metric(label="Digitaalisen kaksosen interaktiot", value="42 kpl", delta="+12 tällä viikolla")

    with tab4:
        render_pricing_engine_ui(asking_price)

if __name__ == "__main__":
    main()
