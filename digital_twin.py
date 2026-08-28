import streamlit as st
from components import render_model_viewer
from database import get_properties
from map_component import render_map_and_services
from agents import render_ai_agent_chat  # <--- Tuodaan olemassa oleva agents.py suoraan käyttöön

def render_digital_twin_view(property_id: int):
    """
    Forman Digitaalinen Kaksonen (Digital Twin) -näkymä.
    Yhdistää LKV-välittäjän hallinnan, kartat, palvelut sekä agents.py:n erilliset asiantuntija-agentit.
    """
    st.markdown("### 🌐 Digitaalinen Kaksonen & Asiakaskohtainen Myynti")
    st.caption("Älykäs digitaalinen kaksonen kytkettynä suoraan Forma-agentteihin ja sijaintitietoihin.")

    # Haetaan kohteen tiedot tietokannasta
    df_props = get_properties()
    property_row = df_props[df_props["id"] == property_id]

    if property_row.empty:
        st.warning("⚠️ Valittua kohdetta ei löytynyt tietokannasta.")
        return

    prop = property_row.iloc[0]
    address = prop["address"]
    asking_price = prop["asking_price"]

    # 1. Välittäjän oma personoitu prompti / aktivointi
    activation_key = f"dt_active_{property_id}"
    is_active = st.session_state.get(activation_key, False)

    st.markdown("#### ⚙️ Välittäjän DigiTwin-ohjaus")
    if not is_active:
        st.info("💡 Aktivoi Digitaalinen Kaksonen tälle kohteelle hallitaksesi asiakaspolkuja.")
        if st.button("🚀 Ota Digitaalinen Kaksonen käyttöön", type="primary"):
            st.session_state[activation_key] = True
            st.success("Digitaalinen kaksonen aktivoitu!")
            st.rerun()
    else:
        st.success("✨ Digitaalinen kaksonen on aktiivinen ja kytketty kohdedataan.")

        # 2. Kartta ja alueen palvelut (Matin ja Annan arjen tukemiseen)
        render_map_and_services(address)

        st.markdown("---")

        # 3. Ostajakohtainen erottelu (Matti, Anna jne.)
        st.markdown("#### 👥 Ostajaehdokkaat ja yksilölliset profiilit")
        st.caption("Erottele ostajat toisistaan, jotta tiedät tarkalleen kuka hakee mitäkin.")

        buyers_key = f"buyers_list_{property_id}"
        if buyers_key not in st.session_state:
            st.session_state[buyers_key] = ["Matti", "Anna"]

        col1, col2 = st.columns([2, 1])
        with col1:
            selected_buyer = st.selectbox("Valitse tarkasteltava ostaja:", st.session_state[buyers_key], key=f"sel_buyer_{property_id}")
        with col2:
            new_buyer_name = st.text_input("Lisää uusi ostaja:", placeholder="Esim. Ville", key=f"new_b_{property_id}")
            if st.button("Lisää ostaja"):
                if new_buyer_name and new_buyer_name not in st.session_state[buyers_key]:
                    st.session_state[buyers_key].append(new_buyer_name)
                    st.rerun()

        st.info(f"🔗 **Uniikki linkki ostajalle ({selected_buyer}):** `forma.fi/kohteet/{property_id}?ostaja={selected_buyer.lower()}`")

        # Ostajakohtainen muisti
        buyer_data_key = f"buyer_profile_{property_id}_{selected_buyer}"
        default_data = {
            "Matti": "Perheeseen tulossa lisäystä, tarvitsee tilaa bändille, huomioi koulut ja arjen sujuvuuden.",
            "Anna": "Hakee skandinaavista sisustustyyliä, haluaa kaataa väliseinän, kiinnostunut pintaremontista."
        }
        current_buyer_info = st.session_state.get(buyer_data_key, default_data.get(selected_buyer, "Ei vielä tietoja."))

        st.markdown(f"##### 📋 Kerätyt tiedot ostajasta: **{selected_buyer}**")
        updated_buyer_info = st.text_area("Asiakkaan profiili ja unelmat:", value=current_buyer_info, key=f"txt_prof_{property_id}_{selected_buyer}")
        if st.button(f"Tallenna {selected_buyer}:n tiedot"):
            st.session_state[buyer_data_key] = updated_buyer_info
            st.success(f"Päivitetty {selected_buyer} tiedot!")

        st.markdown("---")

        # 4. 3D-malli
        st.markdown("#### 📐 Kohteen 3D-malli (Digital Twin Viewer)")
        model_path = st.session_state.get(f"active_glb_{property_id}", "uploads/model.glb")
        render_model_viewer(model_path)

        st.markdown("---")

        # 5. Kutsutaan suoraan olemassa olevaa agents.py -logiikkaa (Sisustaja, Remontti, Kauppa)
        st.markdown(f"#### 🤖 Agenttikeskustelu ({selected_buyer}:n näkymä)")
        st.caption("Valitse alta suoraan oikea asiantuntija-agentti (huomaa: sisustus ja remontti toimivat eri ohjeistuksilla kuten agents.py määrittää).")
        
        # Kutsutaan olemassa olevan agents.py -tiedoston funktiota
        render_ai_agent_chat(property_id=property_id, user_role=selected_buyer)
