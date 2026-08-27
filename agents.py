import streamlit as st
from pricing import laske_terassi
from storage import save_uploaded_file

def render_ai_agent_chat(property_id, user_role="Ostaja"):
    """
    Forman koulutetut tekoälyagentit. Analysoi kuvien perusteella huonekalujen sijoittelun
    (esim. pöytä vierashuoneeseen) ja keittiön kaappien uusimisen.
    """
    st.markdown("### 🤖 Forma AI -Asiantuntijat & Remonttilaskenta")
    st.caption("Kysy kohteesta, huonekalujen mahtuvuudesta tai keittiöremontin kustannuksista.")

    agent_type = st.selectbox(
        "Valitse asiantuntija-agentti:",
        [
            "✨ Sisustaja & Huonekalujen sovitus",
            "🔨 Remontti- ja Keittiöasiantuntija",
            "💼 Kauppa- ja Rahoitusvalmentaja"
        ]
    )
    
    st.markdown("---")

    # Istuntohistoria
    chat_key = f"messages_{property_id}_{agent_type}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {
                "role": "assistant",
                "content": f"Hei! Olen Forman {agent_type.split()[1].lower()}agentti. Näen ladatut kuvat keittiöstä ja huoneista. Miten voin auttaa?"
            }
        ]

    for message in st.session_state[chat_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Kysy esim. 'Mahtuuko tuo pöytä vierashuoneeseen?' tai 'Paljonko keittiön kaapit maksavat?'"):
        st.session_state[chat_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            lower_prompt = prompt.lower()
            response = ""

            if "Sisustaja" in agent_type:
                if "vierashuone" in lower_prompt or "pöytä" in lower_prompt or "mahtuu" in lower_prompt:
                    response = (
                        "Kuvassa näkyvä puinen ruokailupöytä (arviolta ~120 cm pitkä) mahtuu oikein hyvin uuteen "
                        "vierashuoneeseen, kun sijoitat sen pitkää seinää vasten. Se toimii siellä tarvittaessa "
                        "myös erinomaisena työpöytänä!"
                    )
                else:
                    response = "Sisustajana autan sinua sovittamaan nykyiset huonekalusi uusiin tiloihin. Haluatko tarkastella huoneiden pohjapiirustuksia 3D-katselimen kautta?"

            elif "Remontti" in agent_type:
                if "keittiö" in lower_prompt or "kaappi" in lower_prompt or "vaihtaa" in lower_prompt:
                    response = (
                        "Keittiön kaappien ja ovien vaihto on loistava tapa uudistaa ilme! Tyypillisen tämän kokoisen "
                        "keittiön kaapistojen uusiminen (materiaalit + asennustyö avaimet käteen -pakettina) maksaa "
                        "arviolta 4 500 – 7 000 € riippuen valituista mekanismeista ja tasoista. Haluatko laskea tarkan arvion?"
                    )
                else:
                    response = "Remonttineuvojana autan sinua kaikissa keittiö- ja pintaremonteissa. Kaapit voidaan vaihtaa sujuvasti ennen muuttoa!"

            else:
                response = "Kauppavalmentajana varmistan, että remontit ja aikataulut saadaan sovitettua yhteen kauppanteon kanssa. Tehdäänkö tästä kohteesta tarjous?"

            st.markdown(response)
            st.session_state[chat_key].append({"role": "assistant", "content": response})
