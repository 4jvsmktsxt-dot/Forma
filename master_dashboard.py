import streamlit as st
import pandas as pd
from database import get_properties

def render_master_dashboard():
    """Renderöi sinun pääkäyttäjän Master Dashboard -näkymän bisnesanalytiikkaa varten."""
    st.markdown("# 👑 Master Dashboard: Forma-liiketoiminnan komentokeskus")
    st.caption("Tämä näkymä on tarkoitettu konseptin esittelyyn asiakkaille, sijoittajille ja uusien bisnesmahdollisuuksien kehittämiseen.")

    # 1. Pääluvut (Showcase KPI-kortit)
    st.markdown("### 📈 Forma-efekti lyhyesti (Portfolio-laajuinen)")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Keskimääräinen myyntiaika", value="14 pv", delta="-34 pv vs. markkina", delta_color="inverse")
    with col2:
        st.metric(label="Hinnanpitävyys", value="98.4%", delta="+2.1% vs. perinteinen")
    with col3:
        st.metric(label="Keskimääräinen lisämyynti", value="2 450 €", delta="Per kohde")
    with col4:
        st.metric(label="Aktiiviset kohteet", value="12 kpl", delta="Kasvussa 🚀")

    st.markdown("---")

    # 2. Uuden bisneksen kehitystyökalut (Kuluttajakäyttäytymisen trendit)
    st.markdown("### 💡 Uudet bisnesmahdollisuudet datasta")
    st.info(
        "**Markkinadata-analyysi:** Ostajien mikrokyselyjen perusteella **72%** alueen ostajista ilmoittaa haluavansa päivittää keittiön tai pinnat heti oston jälkeen. "
        "Tämä mahdollistaa suoran kumppanimyynnin (esim. keittiöremonttipaketti) myyjille lisäpalveluna."
    )

    # 3. Kohteiden hallinta pääkäyttäjälle
    st.markdown("### 🗂️ Järjestelmän aktiiviset kohteet")
    df_props = get_properties()
    
    if not df_props.empty:
        st.dataframe(df_props, use_container_width=True)
    else:
        st.warning("Ei vielä kohteita tietokannassa. Lisää ensimmäinen kohde järjestelmään!")

    # 4. Työkalu uuden kohteen lisäämiseen Master-näkymästä
    with st.expander("➕ Lisää uusi kohde järjestelmään"):
        from database import add_property
        with st.form("add_prop_form"):
            new_address = st.text_input("Kohteen osoite")
            new_type = st.selectbox("Kohteen tyyppi", ["Kerrostalo", "Rivitalo", "Omakotitalo"])
            new_price = st.number_input("Pyyntihinta (€)", min_value=50000, step=10000, value=250000)
            
            submitted = st.form_submit_button("Tallenna kohde")
            if submitted and new_address:
                add_property(new_address, new_type, new_price)
                st.success(f"Kohde {new_address} lisätty onnistuneesti!")
                st.rerun()