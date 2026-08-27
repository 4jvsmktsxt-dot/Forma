import imaplib
import email
import os
import streamlit as st

EMAIL_USER = "formalkv@gmail.com"
EMAIL_PASS = "uxhd saqo dtyt ankr"  # App Password / Sovellussalasana
IMAP_SERVER = "imap.gmail.com"
DOWNLOAD_FOLDER = "uploads"

def fetch_incoming_attachments():
    """Hakkee sähköpostitse saapuneet tiedostot (esim. kuvat/videot) ja tallentaa ne uploads-kansioon."""
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
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        filename = part.get_filename()
                        if filename:
                            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            fetched_files.append(filepath)

        mail.close()
        mail.logout()
        print("Sähköpostit tarkastettu ja liitteet haettu.")
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

    print(f"Media vastaanotettu ulkoisesta kanavasta: {original_filename}")
    return filepath

def render_ingest_dashboard():
    """Streamlit-käyttöliittymä Ingest Hubille (Master Dashboardin alle)."""
    st.markdown("### 📥 Ingest Hub & Viestiliikenne")
    st.caption("Automaattinen sähköpostien ja mediakuvien tuonti järjestelmään.")

    if st.button("Tarkista sähköpostit ja hae liitteet (Gmail)"):
        with st.spinner("Haetaan liitteitä sähköpostista..."):
            files = fetch_incoming_attachments()
            if files:
                st.success(f"Löytyi ja tallennettiin {len(files)} uutta tiedostoa uploads-kansioon!")
                for f in files:
                    st.write(f"- {f}")
            else:
                st.info("Ei uusia liitteitä tai viestejä.")