import streamlit as st
import pandas as pd
from database import get_properties, init_db, add_property  # Varmista että add_property löytyy database.py:stä
from metrics import render_dynamic_metrics
from buyer_intake import render_buyer_intake
from master_dashboard import render_master_dashboard
from agents import render_ai_agent_chat
from pricing import render_pricing_engine_ui
from ingest_hub import render_ingest_dashboard
from digital_twin import render_digital_twin_view
from map_component import render_map_and_services

init_db()

st.set_page_config(
    page_title="Forma - Kiinteistöresurssien hallinta",
    page_icon="🏠",
    layout="wide"
)

def render_quick_add_property():
    """Näyttää pienen lomakkeen kohteen lisäykseen suoraan tyhjässä näkymässä."""
    with st.expander("➕ Lisää uusi kohde järjestelmään heti"):
        with st.form("quick_add_form"):
            new_address = st.text_input("Kohteen osoite")
            new_price = st.number_input("Velaton hinta / Pyyntihinta (€)", value=250000)
            submitted = st.form_submit_button("Tallenna kohde")
            if submitted and new_address:
                # Tallennetaan tietokantaan (tai kutsutaan sopivaa funktiota)
                try:
                    add_property(new_address, new_price)
                    st.success(f"Kohde '{new_address}' lisätty onnistuneesti! Päivitä sivu.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Virhe tallennuksessa: {e}")

def main():
    st.sidebar.markdown("## 🔒 Forma-kirjautuminen")
    role = st.sidebar.selectbox(
        "Valitse rooli", 
        [
            "LKV-välittäjä", 
            "Remonttimyyjä", 
            "Master Dashboard & Ingest Hub"
        ]
    )
    
    if "LKV-välittäjä" in role:
        st.markdown("# 🏠 LKV-välittäjän työtila")
        st.caption("Kohteiden hallinta, dynaamiset mittarit, hinnoittelu ja ostajakyselyt.")
        
        df_props = get_properties()
        if not df_props.empty:
            selected_prop = st.sidebar.selectbox("Valitse kohde", df_props["address"].tolist(), key="lkv_prop")
            matched_row = df_props.loc[df_props["address"] == selected_prop].iloc[0]
            prop_id = matched_row["id"]
            asking_price = matched_row["asking_price"]
            address = matched_row["address"]

            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🌐 Digitaalinen Kaksonen & Kartta", 
                "📊 Analytiikka & Kysely", 
                "💰 Hinnoittelu & Laskuri", 
                "🤖 AI-Agentit", 
                "🏡 Ostajan mikrokysely"
            ])
            
            with tab1:
                render_map_and_services(address)
                st.markdown("---")
                render_digital_twin_view(prop_id)
            with tab2:
                render_dynamic_metrics(prop_id)
            with tab3:
                render_pricing_engine_ui(asking_price)
            with tab4:
                render_ai_agent_chat(prop_id, user_role="LKV")
            with tab5:
                render_buyer_intake(prop_id)
        else:
            st.warning("Ei aktiivisia kohteita järjestelmässä.")
            render_quick_add_property()

    elif "Remonttimyyjä" in role:
        st.markdown("# 🔨 Remonttimyyjän työtila")
        st.caption("Ostajien remonttialttuus, liukusäädinmetriikat ja lisämyyntipaketit.")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚙️ Remontti-agentin asetukset")
        custom_strength = st.sidebar.text_input(
            "Syötä omat vahvuudet / prompti", 
            value="Erikoisosaaminen: Nopea putkiremontti ja mittatilaustasot",
            key="remot_strength_input"
        )

        df_props = get_properties()
        if not df_props.empty:
            selected_prop = st.sidebar.selectbox("Valitse kohde", df_props["address"].tolist(), key="remontti_prop")
            matched_row = df_props.loc[df_props["address"] == selected_prop].iloc[0]
            prop_id = matched_row["id"]
            asking_price = matched_row["asking_price"]
            address = matched_row["address"]

            tab1, tab2, tab3, tab4 = st.tabs([
                "🌐 Remontin Digitaalinen Kaksonen", 
                "💰 Remontti- ja lisämyyntilaskuri", 
                "📊 Ostajadata", 
                "🤖 AI-Remonttiassistentti"
            ])
            
            with tab1:
                render_map_and_services(address)
                st.markdown("---")
                render_digital_twin_view(prop_id)
            with tab2:
                render_pricing_engine_ui(asking_price)
            with tab3:
                render_dynamic_metrics(prop_id)
            with tab4:
                render_ai_agent_chat(prop_id, user_role="Remonttimyyjä", custom_system_prompt=custom_strength)
        else:
            st.warning("Ei aktiivisia kohteita järjestelmässä.")
            render_quick_add_property()

    elif "Master Dashboard & Ingest Hub" in role:
        render_master_dashboard()
        st.markdown("---")
        render_ingest_dashboard()

if __name__ == "__main__":
    main()
