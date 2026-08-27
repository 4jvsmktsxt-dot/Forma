import streamlit as st
from database import init_db, get_properties
from buyer_intake import render_buyer_intake
from metrics import render_dynamic_metrics
from master_dashboard import render_master_dashboard

# Sivun perusasetukset
st.set_page_config(
    page_title="Forma | Kiinteistö- ja Remonttialusta",
    page_icon="🏠",
    layout="wide"
)

# Alustetaan tietokanta taustalla automaattisesti
init_db()

def main():
    # Sivupalkki (Sidebar) roolin valintaan ja kirjautumiseen
    st.sidebar.markdown("## 🔐 Forma-kirjautuminen")
    st.sidebar.caption("Valitse roolisi ja näkymäsi järjestelmässä.")

    # Simuloitu kirjautuminen / roolivalitsin
    role = st.sidebar.selectbox(
        "Käyttäjärooli",
        [
            "👑 Master Dashboard (Pääkäyttäjä / Toni)",
            "📋 LKV-välittäjä",
            "🔨 Remonttimyyjä"
        ]
    )

    st.sidebar.markdown("---")

    # Roolipohjainen näkymän ohjaus
    if "Master Dashboard" in role:
        # Sinun pääkäyttäjän komentokeskus
        render_master_dashboard()

    elif "LKV-välittäjä" in role:
        st.markdown("# 📋 LKV-välittäjän työtila")
        st.caption("Ostajapoolin seuranta, hinnanpitävyys ja klousausvinkit.")

        # Valitaan kohde, jota tarkastellaan
        df_props = get_properties()
        if not df_props.empty:
            selected_prop = st.sidebar.selectbox("Valitse kohde", df_props["address"].tolist())
            prop_id = df_props.loc[df_props["address"] == selected_prop, "id"].values[0]

            # Näytetään dynaamiset mittarit ja ostajan mikrokyselynäkymä
            render_dynamic_metrics(prop_id)
            st.markdown("---")
            render_buyer_intake(prop_id)
        else:
            st.warning("Ei aktiivisia kohteita. Siirry Master Dashboardiin lisäämään ensimmäinen kohde.")

    elif "Remonttimyyjä" in role:
        st.markdown("# 🔨 Remonttimyyjän työtila")
        st.caption("Ostajien remonttialttuus, liukusäädinmetriikat ja lisämyyntipaketit.")

        df_props = get_properties()
        if not df_props.empty:
            selected_prop = st.sidebar.selectbox("Valitse kohde", df_props["address"].tolist())
            prop_id = df_props.loc[df_props["address"] == selected_prop, "id"].values[0]

        # Remonttimyyjälle nostetaan esiin erityisesti dynaamiset mittarit ja ostajakyselyt
        render_dynamic_metrics(prop_id)
        st.markdown("---")
        render_buyer_intake(prop_id)
        else:
            st.warning("Ei aktiivisia kohteita järjestelmässä.")

if __name__ == "__main__":
    main()
