import streamlit as st
import datetime
from typing import Dict, List

# Simuloitu tietokanta / tila (tuotannossa korvataan tietokannalla, esim. PostgreSQL)
if "db_customers" not in st.session_state:
    st.session_state.db_customers = [
        {"name": "Matti Meikäläinen", "company": "SuperLKV Oy", "business_id": "1234567-8", "email": "matti@superlkv.fi", "phone": "+358401234567", "credits": 15, "status": "Active"},
        {"name": "Maija Mallikas", "company": "Design Remontti Oy", "business_id": "8765432-1", "email": "maija@designremontti.fi", "phone": "+358509876543", "credits": 5, "status": "Active"}
    ]

if "db_campaigns" not in st.session_state:
    st.session_state.db_campaigns = [
        {"code": "SYKSYLKV2026", "discount": "20%", "uses": 12, "active": True},
        {"code": "PILOTVIP", "discount": "Ilmainen kuukausi", "uses": 3, "active": True}
    ]

def render_master_dashboard():
    """
    Omistajan Master Dashboard -komentokeskus.
    Vain sinun näkymäsi (pääkäyttäjä).
    """
    st.title("👑 Master Dashboard – Omistajan Komentokeskus")
    st.markdown("Reaaliaikainen näkymä asiakkaista, lisensseistä, kampanjoista ja järjestelmän tilasta.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Asiakasrekisteri & B2B", "🎟️ Kampanjat & Alennukset", "🔗 Invite-linkit", "⚡ Webhook & Maksu-lokit"])

    # --- TAB 1: ASIAKASREKISTERI & B2B ---
    with tab1:
        st.subheader("Aktiiviset asiakkaat ja yritykset")
        
        # Näytetään asiakkaat taulukkona
        customer_data = st.session_state.db_customers
        st.dataframe(customer_data, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Yrityksen (Pomon) näkymän simulaatio")
        selected_company = st.selectbox("Valitse yritys tarkasteluun", [c["company"] for c in customer_data])
        
        # Suodatetaan yrityksen mukaan
        company_users = [c for c in customer_data if c["company"] == selected_company]
        st.info(f"Yritys: **{selected_company}** | Aktiivisia tekijöitä: {len(company_users)} | Yhteiset käyttöoikeudet (krediitit): {sum(c['credits'] for c in company_users)}")

    # --- TAB 2: KAMPANJAT & ALENNUKSET ---
    with tab2:
        st.subheader("Kampanjoiden ja alennuskoodien hallinta")
        
        with st.form("new_campaign_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_code = st.text_input("Kampanjakoodi (esim. KEVAT2026)")
            with col2:
                new_discount = st.text_input("Alennus / Etu (esim. -30% tai +10 krediittiä)")
            
            submit_campaign = st.form_submit_button("Luo uusi kampanja / alennus")
            if submit_campaign and new_code:
                st.session_state.db_campaigns.append({"code": new_code.upper(), "discount": new_discount, "uses": 0, "active": True})
                st.success(f"Kampanja {new_code.upper()} luotu onnistuneesti!")

        st.markdown("### Olemassa olevat kampanjat")
        st.dataframe(st.session_state.db_campaigns, use_container_width=True)

    # --- TAB 3: INVITE-LINKIT & YKSILÖKOHTAISET TARJOUKSET ---
    with tab3:
        st.subheader("Generoi henkilökohtainen Invite-linkki / Kutsulinkki")
        st.markdown("Voit lähettää tämän linkin suoraan yksittäiselle LKV-välittäjälle tai pomolle. Linkki esitäyttää tiedot ja voi sisältää räätälöidyn alennuksen.")

        with st.form("invite_form"):
            invite_name = st.text_input("Välittäjän / Yhteyshenkilön nimi")
            invite_email = st.text_input("Sähköposti")
            invite_company = st.text_input("Yrityksen nimi (valinnainen)")
            assigned_campaign = st.selectbox("Liitä kampanja/alennus linkille", [c["code"] for c in st.session_state.db_campaigns])
            
            generate_btn = st.form_submit_button("Generoi Invite-linkki")
            if generate_btn and invite_email:
                # Tehdään simuloitu token-linkki
                invite_link = f"https://forma.fi/register?email={invite_email}&promo={assigned_campaign}"
                st.success("Kutsulinkki luotu!")
                st.code(invite_link, language="text")

    # --- TAB 4: WEBHOOK & MAKSULOKIT ---
    with tab4:
        st.subheader("Stripe / Maksuliikenteen Webhook-tila")
        st.markdown("Kun asiakas suorittaa maksun, Stripe lähettää tänne automaattisen signaalin, joka aktivoi tilin välittömästi.")
        
        # Simuloitu webhook-status
        st.success("🟢 Webhook-kuuntelija (`/api/webhook/stripe`) aktiivinen ja valmiina portissa 443.")
        
        if st.button("Simuloi saapuva maksu (Webhook Test)"):
            st.info("Simuloitu maksu vastaanotettu: Uusi tili luotu automaattisesti taustalla ja krediitit lisätty.")

if __name__ == "__main__":
    render_master_dashboard()
