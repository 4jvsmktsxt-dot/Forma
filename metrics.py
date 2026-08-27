import streamlit as st
from database import save_buyer_response

def render_buyer_intake(property_id):
    """Renderöi ostajan mikrokyselyn (liukusäätimet ja monivalinnat) 3D-näkymän tai chatin yhteyteen."""
    st.markdown("### 🏡 Mikrokysely ostajalle")
    st.caption("Auta meitä räätälöimään kokemus tarpeisiisi vetämällä liukusäätimiä tai valitsemalla vaihtoehdot.")

    with st.form(key=f"buyer_intake_form_{property_id}"):
        
        # 1. Kiireellisyys / Muuttoaikataulu (Liukusäädin 1-10)
        timeline_score = st.slider(
            "Kuinka kiireellinen muutostarpeesi on?",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Haeskelen vain rauhassa yli 6 kk päästä, 10 = Pakko päästä muuttamaan heti!"
        )

        # 2. Rahoituksen tila (Monivalinta)
        financing_status = st.selectbox(
            "Mikä on rahoituksesi tila tällä hetkellä?",
            [
                "Lainalupaus taskussa / valmiina",
                "Pankkineuvottelut kesken",
                "En ole vielä aloittanut prosessia"
            ]
        )

        # 3. Remonttialttuus / Omat toiveet (Liukusäädin 1-10)
        renovation_readiness = st.slider(
            "Kuinka valmis olet tekemään pinnan- tai tilamuutoksia (esim. keittiö/kylpyhuone)?",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Kaiken pitää olla heti valmista, 10 = Haluan toteuttaa täydellisen remontin omien makujen mukaan."
        )

        # 4. Suurin huoli tai pelko (Tekstikenttä tai lyhyt valinta)
        main_concern = st.text_input(
            "Mikä asunnossa tai taloyhtiössä eniten mietityttää?",
            placeholder="Esim. tulevat remontit, keittiön toimivuus, sijainti..."
        )

        # Lähetä-painike
        submit_button = st.form_submit_button(label="Tallenna tiedot ja siirry 3D/Chat-tilaan 🚀")

        if submit_button:
            save_buyer_response(
                property_id=property_id,
                timeline_score=timeline_score,
                financing_status=financing_status,
                renovation_readiness=renovation_readiness,
                main_concern=main_concern
            )
            st.success("Kiitos! Tiedot tallennettu onnistuneesti järjestelmään.")
            st.balloons()