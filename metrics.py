import streamlit as st
import pandas as pd
from database import get_buyer_responses

def render_dynamic_metrics(property_id):
    """Renderöi kohteen dynaamiset mittarit ja ostajakyselyn yhteenvedon."""
    st.markdown("### 📊 Kohteen dynaamiset mittarit & Ostajadata")
    st.caption("Reaaliaikainen analytiikka ostajien mikrokyselyistä ja kiinteistön potentiaalista.")

    # Haetaan tietokannasta kyseisen kohteen ostajavastaukset
    df_responses = get_buyer_responses(property_id)

    if not df_responses.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_timeline = df_responses["timeline_score"].mean()
            st.metric(label="Keskimääräinen kiireellisyys", value=f"{avg_timeline:.1f} / 10")
        with col2:
            avg_renovation = df_responses["renovation_readiness"].mean()
            st.metric(label="Keskimääräinen remonttialttuus", value=f"{avg_renovation:.1f} / 10")
        with col3:
            total_responses = len(df_responses)
            st.metric(label="Kyselyn vastauksia", value=f"{total_responses} kpl")

        st.markdown("---")
        st.markdown("#### 💬 Viimeisimmät ostajien huolet ja kommentit:")
        for index, row in df_responses.tail(3).iterrows():
            st.info(f"**Asiakkaan huoli:** {row['main_concern']} *(Rahoitustila: {row['financing_status']})*")
    else:
        st.info("ℹ️ Ei vielä ostajavastauksia tälle kohteelle. Kun ostajat täyttävät mikrokyselyn, dynaamiset mittarit päivittyvät tähän reaaliajassa.")
