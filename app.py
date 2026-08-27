import streamlit as st
import pandas as pd
from database import get_properties, add_property
from metrics import render_dynamic_metrics
from buyer_intake import render_buyer_intake

st.set_page_config(
    page_title="Forma - Kiinteistöresurssien hallinta",
    page_icon="🏠",
    layout="wide"
)

def main():
    st.sidebar.markdown("## 🔒 Forma-kirjautuminen")
    role = st.sidebar.selectbox("Valitse rooli", ["LKV-välittäjä", "Remonttimyyjä", "Master Dashboard"])
    
    if "LKV-välittäjä" in role:
        st.markdown("# 🏠 LKV-välittäjän työtila")
        st.caption("Kohteiden hallinta, dynaamiset mittarit ja ostajakyselyt.")
        
        df_props = get_properties()
        if not df_props.empty:
            selected_prop = st.sidebar.selectbox("Valitse kohde", df_props["address"].tolist(), key="lkv_prop")
            prop_id = df_props.loc[df_props["address"] == selected_prop, "id"].values[0]

            render_dynamic_metrics(prop_id)
            st.markdown("---")
            render_buyer_intake(prop_id)
        else:
            st.warning("Ei aktiivisia kohteita järjestelmässä. Siirry Master Dashboardiin lisäämään ensimmäinen kohde.")

    elif "Remonttimyyjä" in role:
        st.markdown("# 🔨 Remonttimyyjän työtila")
        st.caption("Ostajien remonttialttuus, liukusäädinmetriikat ja lisämyyntipaketit.")
        
        df_props = get_properties()
        if not df_props.empty:
            selected_prop = st.sidebar.selectbox("Valitse kohde", df_props["address"].tolist(), key="remontti_prop")
            prop_id = df_props.loc[df_props["address"] == selected_prop, "id"].values[0]

            render_dynamic_metrics(prop_id)
            st.markdown("---")
            render_buyer_intake(prop_id)
        else:
            st.warning("Ei aktiivisia kohteita järjestelmässä.")

    elif "Master Dashboard" in role:
        st.markdown("# 📊 Master Dashboard")
        st.caption("Järjestelmän laaja näkymä ja hallinta.")
        
        st.markdown("### Lisää uusi kohde")
        with st.form("add_prop_form"):
            new_address = st.text_input("Kohteen osoite")
            new_price = st.number_input("Velaton hinta (€)", min_value=0.0, step=1000.0)
            submitted = st.form_submit_button("Tallenna kohde")
            
            if submitted and new_address:
                add_property(new_address, new_price)
                st.success(f"Kohde '{new_address}' lisätty onnistuneesti!")
                st.rerun()

if __name__ == "__main__":
    main()
