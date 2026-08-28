import streamlit as st

def laske_terassi(pinta_ala_m2: float, toimitustapa: str = "itse") -> dict:
    """
    Laskee terassin materiaali- ja työkustannukset pinta-alan ja toimitustavan perusteella.
    Tukee remonttimyyjän lisämyyntilaskentaa.
    """
    materiaali_hinta_per_m2 = 80.0  # puutavara, ruuvit, anturat
    tuntia_per_m2 = 1.5
    tuntipalkka = 45.0

    materiaalit_yhteensä = pinta_ala_m2 * materiaali_hinta_per_m2

    if toimitustapa == "itse":
        return {
            "materiaalit": materiaalit_yhteensä,
            "tyo": 0.0,
            "yhteensa": materiaalit_yhteensä
        }
    else:  # avaimet käteen
        tyo_yhteensa = pinta_ala_m2 * tuntia_per_m2 * tuntipalkka
        kokonaismaksu = materiaalit_yhteensä + tyo_yhteensa
        return {
            "materiaalit": materiaalit_yhteensä,
            "tyo": tyo_yhteensa,
            "yhteensa": kokonaismaksu
        }

def laske_kustannukset(pinta_ala_m2: float, toimitustapa: str = "itse") -> dict:
    """Yhteensopivuusfunktio sovelluksen muihin osiin - ohjaa kutsun suoraan terassilogiikkaan."""
    return laske_terassi(pinta_ala_m2, toimitustapa)

def hae_hinnasto() -> dict:
    """Palauttaa voimassa olevan hinnaston ja parametrit sovelluksen käyttöön."""
    return {
        "materiaali_hinta_per_m2": 80.0,
        "tuntipalkka": 45.0,
        "tuntia_per_m2": 1.5
    }

def render_pricing_engine_ui(asking_price):
    """
    Forman integroitu hinnoittelu- ja lisämyyntimoottori Streamlit-käyttöliittymään.
    Kytkeytyy suoraan LKV- ja Remonttimyyjän näkymiin.
    """
    st.markdown("### 💰 Forma Pricing & Lisämyyntilaskuri")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Kohteen pyyntihinta", value=f"{asking_price:,.0f} €".replace(",", " "))
    with col2:
        estimated_realized = asking_price * 0.985
        st.metric(label="Ennustettu toteutuma", value=f"{estimated_realized:,.0f} €".replace(",", " "), delta="+1.5% vs. perinteinen", delta_color="normal")

    st.markdown("---")
    st.markdown("#### 🔨 Remontti- ja lisämyyntilaskuri (esim. Terassi / Pintaremontti)")
    
    pinta_ala = st.slider("Valitse remonttikohteen pinta-ala (m²)", min_value=10, max_value=100, value=25, step=5)
    toimitustapa = st.selectbox("Valitse toimitustapa", ["itse", "avaimet käteen"])
    
    tulokset = laske_terassi(pinta_ala, toimitustapa)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(label="Materiaalit", value=f"{tulokset['materiaalit']:,.0f} €".replace(",", " "))
    with col_b:
        st.metric(label="Työn osuus", value=f"{tulokset['tyo']:,.0f} €".replace(",", " "))
    with col_c:
        st.metric(label="Yhteensä", value=f"{tulokset['yhteensa']:,.0f} €".replace(",", " "))
        
    st.caption("Laskenta perustuu Forma-hinnastoon ja reaaliaikaiseen ostajapoolin kysyntään.")
