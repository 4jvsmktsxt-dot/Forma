import streamlit as st
import pandas as pd
from database import get_properties, init_db
from metrics import render_dynamic_metrics
from buyer_intake import render_buyer_intake
from master_dashboard import render_master_dashboard
from agents import render_ai_agent_chat
from pricing import render_pricing_engine_ui
from ingest_hub import render_ingest_dashboard

# Alustetaan tietokanta heti käynnistyksessä
init_db()

st.set_page_config(
    page_title="Forma - Kiinteistöresurssien hallinta",
    page_icon="🏠",
    layout="wide"
)

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

            # Välilehdet LKV-näkymään
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytiikka & Kysely", "💰 Hinnoittelu & Laskuri", "🤖 AI-Agentit", "🏡 Ostajan mikrokysely"])
            
            with tab1:
                render_dynamic_metrics(prop_id)
            with tab2:
                render_pricing_engine_ui(asking_price)
            with tab3:
                render_ai_agent_chat(prop_id, user_role="LKV")
            with tab4:
                render_buyer_intake(prop_id)
        else:
            st.warning("Ei aktiivisia kohteita järjestelmässä. Siirry Master Dashboardiin lisäämään ensimmäinen kohde.")

    elif "Remonttimyyjä" in role:
        st.markdown("# 🔨 Remonttimyyjän työtila")
        st.caption("Ostajien remonttialttuus, liukusäädinmetriikat ja lisämyyntipaketit.")
        
        df_props = get_properties()
        if not df_props.empty:
            selected_prop = st.sidebar.selectbox("Valitse kohde", df_props["address"].tolist(), key="remontti_prop")
            matched_row = df_props.loc[df_props["address"] == selected_prop].iloc[0]
            prop_id = matched_row["id"]
            asking_price = matched_row["asking_price"]

            tab1, tab2, tab3 = st.tabs(["💰 Remontti- ja lisämyyntilaskuri", "📊 Ostajadata", "🤖 AI-Remonttiassistentti"])
            
            with tab1:
                render_pricing_engine_ui(asking_price)
            with tab2:
                render_dynamic_metrics(prop_id)
            with tab3:
                render_ai_agent_chat(prop_id, user_role="Remonttimyyjä")
        else:
            st.warning("Ei aktiivisia kohteita järjestelmässä.")

    elif "Master Dashboard & Ingest Hub" in role:
        # Renderöidään Master Dashboard
        render_master_dashboard()
        st.markdown("---")
        # Renderöidään myös Ingest Hub (Sähköpostit ja mediatoisinnat)
        render_ingest_dashboard()

if __name__ == "__main__":
    main()
