import imaplib
import email
from email.header import decode_header
import os
import streamlit as st

EMAIL_USER = "formalkv@gmail.com"
EMAIL_PASS = "uxhd saqo dtyt ankr"  # App Password / Sovellussalasana
IMAP_SERVER = "imap.gmail.com"
DOWNLOAD_FOLDER = "uploads"

def fetch_incoming_attachments():
    """Hakee sähköpostitse saapuneet tiedostot (kuvat/videot) ja palauttaa listan tiedostoista ja lähettäjistä."""
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    fetched_files = []
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Etsitään lukemattomat viestit
        status, messages = mail.search(None, 'UNSEEN')
        
        if status != 'OK':
            return fetched_files

        for num in messages[0].split():
            res, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = msg.get("From", "Tuntematon lähettäjä")
                    
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        filename = part.get_filename()
                        if filename:
                            # Puretaan mahdollinen koodattu tiedostonimi
                            decoded_header = decode_header(filename)
                            filename, encoding = decoded_header[0]
                            if isinstance(filename, bytes):
                                filename = filename.decode(encoding if encoding else "utf-8", errors="ignore")

                            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            
                            fetched_files.append({"file": filepath, "sender": sender})

        mail.close()
        mail.logout()
    except Exception as e:
        print(f"Virhe sähköpostin haussa: {e}")
        
    return fetched_files

def handle_incoming_media(file_data, original_filename):
    """
    Yleinen rajapinta WhatsAppista tai muusta ulkoisesta järjestelmästä tulleille tiedostoille.
    Tänne ohjataan käyttäjien puhelimilla kuvaamat videot ja kuvat.
    """
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    filepath = os.path.join(DOWNLOAD_FOLDER, original_filename)
    with open(filepath, "wb") as f:
        f.write(file_data)

    return filepath

def render_ingest_dashboard():
    """Streamlit-käyttöliittymä Ingest Hubille (Master Dashboardin alle)."""
    st.markdown("### 📥 Ingest Hub & Viestiliikenne")
    st.caption("Keskitetty hallinta saapuville pohjapiirroksille, kuville ja videoille.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Tarkista sähköpostit (Gmail)", use_container_width=True):
            with st.spinner("Haetaan uusia liitteitä..."):
                files = fetch_incoming_attachments()
                if files:
                    st.success(f"Löytyi ja tallennettiin {len(files)} uutta tiedostoa!")
                    for item in files:
                        st.write(f"- **{os.path.basename(item['file'])}** *(Lähettäjä: {item['sender']})*")
                else:
                    st.info("Ei uusia viestejä tai liitteitä laatikossa.")

    st.markdown("---")
    st.markdown("#### 📂 Aktiiviset tiedostot `uploads/`-kansiossa")
    
    if os.path.exists(DOWNLOAD_FOLDER):
        files_in_folder = os.listdir(DOWNLOAD_FOLDER)
        if files_in_folder:
            file_data = []
            for f in files_in_folder:
                f_path = os.path.join(DOWNLOAD_FOLDER, f)
                if os.path.isfile(f_path):
                    file_data.append({
                        "Tiedostonimi": f,
                        "Koko (kt)": round(os.path.getsize(f_path) / 1024, 1)
                    })
            st.dataframe(file_data, use_container_width=True)
        else:
            st.info("Kansio on tällä hetkellä tyhjä.")
    else:
        st.info("Uploads-kansiota ei ole vielä luotu järjestelmään.")
