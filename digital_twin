import streamlit as st
from components import render_model_viewer
from database import get_properties

def render_digital_twin_view(property_id: int):
    """
    Forman Digitaalinen Kaksonen (Digital Twin) -näkymä LKV-välittäjille ja remonttimyyjille.
    Aktivoi Master Dashboardista määritetyn ydinpromptin ja yhdistää sen 3D-katselimeen ja tekoälyyn.
    """
    st.markdown("### 🌐 Digitaalinen Kaksonen & Älykäs Kohdekatselin")
    st.caption("Interaktiivinen 3D-malli, kohdekohtainen tekoälyavustaja ja reaaliaikainen ohjaus.")

    # Haetaan kohteen tiedot tietokannasta
    df_props = get_properties()
    property_row = df_props[df_props["id"] == property_id]

    if property_row.empty:
        st.warning("⚠️ Valittua kohdetta ei löytynyt tietokannasta.")
        return

    prop = property_row.iloc[0]
    address = prop["address"]
    asking_price = prop["asking_price"]

    # Master Dashboardista määritetty ydinprompti (simuloidaan sessiosta / tallennuksesta)
    default_master_prompt = (
        f"Olet Forma-kohdeasiantuntija kohteessa {address}. "
        f"Pyyntihinta on {asking_price:,.0f} €. Korosta kaupallisessa viestinnässä "
        f"kohteen muuntojoustavuutta, nopeutta ja remontti-integraation mahdollisuuksia."
    ).replace(",", " ")
    
    master_prompt = st.session_state.get(f"master_prompt_{property_id}", default_master_prompt)

    # LKV-välittäjän / remonttimyyjän aktivointinäkymä
    activation_key = f"dt_active_{property_id}"
    is_active = st.session_state.get(activation_key, False)

    if not is_active:
        st.info(
            f"💡 **Kohde valmiina aktivointiin:** Pääkäyttäjä on määrittänyt tälle kohteelle Master-tason ohjeistuksen. "
            f"Voit ottaa Digitaalisen Kaksosen käyttöön omasta profiilistasi alta."
        )
        if st.button("🚀 Ota Digitaalinen Kaksonen käyttöön", type="primary"):
            st.session_state[activation_key] = True
            st.success("Digitaalinen kaksonen aktivoitu onnistuneesti!")
            st.rerun()
    else:
        st.success("✨ Digitaalinen kaksonen on aktiivinen ja kytketty kohdedataan.")

        # Näytetään Masterin antama ydinprompti suljetussa laatikossa
        with st.expander("👑 Pääkäyttäjän asettama Master-ydinprompti"):
            st.write(master_prompt)

        # 3D-mallin katselin (käyttää olemassa olevaa components.py -moduulia)
        st.markdown("#### 📐 Kohteen 3D-malli (Digital Twin Viewer)")
        model_path = st.session_state.get(f"active_glb_{property_id}", "uploads/model.glb")
        render_model_viewer(model_path)

        st.markdown("---")
        st.markdown("#### 💬 Kysy Digitaaliselta Kaksoselta")
        user_prompt = st.text_input(
            "Testaa promptia (esim. 'Mahtuuko tähän olohuoneeseen iso kulmasohva?' tai 'Mitä maksaa pintaremontti?'):",
            key=f"chat_input_{property_id}"
        )

        if user_prompt:
            with st.spinner("Digitaalinen kaksonen analysoi kohdetta..."):
                # Vastataan Master-promptin ohjaamana (integroidaan agents.py logiikkaan tuotannossa)
                response = (
                    f"🤖 **Forma AI (perustuu Master-ohjeistukseen):** "
                    f"Analysoiden kohdetta *{address}* kysymykseesi *\"{user_prompt}\"* voidaan todeta, "
                    f"että tila tarjoaa erinomaiset puitteet ja joustavuuden muutoksille."
                )
                st.markdown(response)
