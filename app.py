import streamlit as st
import pandas as pd
from database import get_properties, init_db, add_property, authenticate_user, add_user, get_all_users
from metrics import render_dynamic_metrics
from buyer_intake import render_buyer_intake
from master_dashboard import render_master_dashboard
from agents import render_ai_agent_chat
from pricing import render_pricing_engine_ui
from ingest_hub import render_ingest_dashboard
from digital_twin import render_digital_twin_view
from map_component import render_map_and_services
from storage import save_uploaded_file

init_db()

st.set_page_config(
    page_title="Forma - Digitaalinen LKV-hallintapaneeli",
    page_icon="🏠",
    layout="wide"
)

def check_login():
    """Tarkistaa kirjautumisen tietokantaa vasten."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.session_state["user_name"] = None
        st.session_state["user_role"] = None

    if not st.session_state["authenticated"]:
        st.markdown("# 🔒 Forma - Kirjaudu sisään")
        st.caption("Syötä käyttäjätunnus ja salasana jatkaaksesi työtilaan.")
        
        with st.form("login_form"):
            username_input = st.text_input("Käyttäjätunnus")
            password_input = st.text_input("Salasana", type="password")
            submit_button = st.form_submit_button("Kirjaudu sisään")
            
            if submit_button:
                user = authenticate_user(username_input, password_input)
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = user["username"]
                    st.session_state["user_name"] = user["name"]
                    st.session_state["user_role"] = user["role"]
                    st.success(f"Tervetuloa, {user['name']}!")
                    st.rerun()
                else:
                    st.error("Virheellinen käyttäjätunnus tai salasana.")
        return False
    return True

def render_user_management():
    """Mahdollistaa uusien käyttäjien lisäämisen suoraan Master-näkymästä."""
    st.markdown("### 👥 Käyttäjien hallinta")
    st.caption("Lisää uusia välittäjiä tai hallitse olemassa olevia tunnuksia.")
    
    # Näytetään olemassa olevat käyttäjät
    df_users = get_all_users()
    st.dataframe(df_users, use_container_width=True)
    
    with st.form("add_user_form"):
        st.markdown("#### Lisää uusi käyttäjä")
        new_username = st.text_input("Käyttäjätunnus (esim. liisa)")
        new_password = st.text_input("Salasana", type="password")
        new_fullname = st.text_input("Koko nimi (esim. Liisa LKV)")
        new_role = st.selectbox("Rooli", ["LKV", "Master"])
        
        submitted = st.form_submit_button("Luo käyttäjätunnus")
        if submitted:
            if new_username and new_password and new_fullname:
                success = add_user(new_username, new_password, new_fullname, new_role)
                if success:
                    st.success(f"Käyttäjä '{new_fullname}' luotu onnistuneesti!")
                    st.rerun()
                else:
                    st.error("Käyttäjätunnus on jo olemassa.")
            else:
                st.warning("Täytä kaikki kentät.")

def render_quick_add_property(current_user_name):
    with st.expander("➕ Lisää uusi kohde järjestelmään"):
        with st.form(f"quick_add_form_{current_user_name}"):
            new_address = st.text_input("Kohteen osoite")
            prop_type = st.selectbox("Kohteen tyyppi", ["Kerrostalo", "Rivitalo", "Omakotitalo"])
            new_price = st.number_input("Velaton hinta / Pyyntihinta (€)", value=250000)
            submitted = st.form_submit_button("Tallenna kohde")
            if submitted and new_address:
                try:
                    add_property(address=new_address, asking_price=new_price, property_type=prop_type, owner=current_user_name)
                    st.success(f"Kohde '{new_address}' lisätty onnistuneesti!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Virhe tallennuksessa: {e}")

def render_media_upload_section(prop_id):
    st.markdown("### 📤 Raahaa ja lataa videot / mediakuvat kohteelle")
    uploaded_files = st.file_uploader(
        "Valitse videot (mp4, mov) tai panoraamakuvat (jpg, png)", 
        type=["mp4", "mov", "jpg", "jpeg", "png"], 
        accept_multiple_files=True,
        key=f"media_upload_{prop_id}"
    )
    
    if uploaded_files:
        if st.button("Tallenna mediasisällöt", key=f"save_media_{prop_id}"):
            for file in uploaded_files:
                try:
                    save_uploaded_file(prop_id, file)
                except Exception:
                    pass
            st.success(f"Tallennettiin {len(uploaded_files)} tiedostoa onnistuneesti!")

def main():
    if not check_login():
        return

    st.sidebar.markdown(f"## 👤 Kirjautunut:")
    st.sidebar.info(f"**{st.session_state['user_name']}**")
    
    if st.sidebar.button("Kirjaudu ulos"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()

    current_user_name = st.session_state["user_name"]
    user_role = st.session_state["user_role"]

    if user_role == "LKV":
        st.markdown(f"# 🌟 {current_user_name} - Myynti- ja hallintapaneeli")
        st.caption("Tehosta myyntiä digitaalisen kaksosen, videoiden ja reaaliaikaisten työkalujen avulla.")
        
        df_props = get_properties(owner=current_user_name)
        
        if not df_props.empty:
            selected_prop = st.sidebar.selectbox("Valitse kohde", df_props["address"].tolist(), key=f"prop_select_{current_user_name}")
            matched_row = df_props.loc[df_props["address"] == selected_prop].iloc[0]
            prop_id = matched_row["id"]
            asking_price = matched_row["asking_price"]
            address = matched_row["address"]

            st.info(f"Aktiivinen kohde: **{address}** (Pyydetty hinta: {asking_price:,.0f} €)")

            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📹 Videot & Media (Aloita tästä)", 
                "🌐 Digitaalinen Kaksonen & Kartta", 
                "📊 Analytiikka & Kyselyt", 
                "💰 Hinnoittelu & Remonttilaskuri", 
                "🤖 AI-Asiantuntija-agentit", 
                "🏡 Ostajan mikrokysely"
            ])
            
            with tab1:
                render_media_upload_section(prop_id)
            with tab2:
                render_map_and_services(address)
                st.markdown("---")
                render_digital_twin_view(prop_id)
            with tab3:
                render_dynamic_metrics(prop_id)
            with tab4:
                render_pricing_engine_ui(asking_price)
            with tab5:
                render_ai_agent_chat(prop_id, user_role=current_user_name)
            with tab6:
                render_buyer_intake(prop_id)
        else:
            st.warning(f"Ei vielä kohteita käyttäjälle {current_user_name}. Lisää ensimmäinen kohde alta:")
            render_quick_add_property(current_user_name)

    elif user_role == "Master":
        render_master_dashboard()
        st.markdown("---")
        render_user_management()
        st.markdown("---")
        render_ingest_dashboard()

if __name__ == "__main__":
    main()
