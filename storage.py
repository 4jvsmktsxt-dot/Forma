import os
import uuid
import shutil
import requests
import streamlit as st

UPLOAD_DIR = "uploads"

def save_uploaded_file(uploaded_file):
    """
    Tallentaa Streamlitistä tulleen tiedoston 'uploads'-kansioon.
    Palauttaa tallennetun tiedoston polun.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    # Luodaan uniikki tiedostonimi, jotta versiot eivät ylikirjoita toisiaan
    unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return file_path

def delete_file(file_path):
    """Poistaa tiedoston levyltä, jos se on olemassa."""
    if os.path.exists(file_path):
        os.remove(file_path)

def convert_video_to_3d(file_path):
    """
    Muuntaa WhatsAppista tai kamerasta tulleen videon/kuvan 3D (.glb) -muotoon.
    Hyödyntää tekoälypohjaista 3D-konversiota (esim. Meshy / Tripo / Luma API).
    """
    # Esimerkki API-integraation rungosta (kytketään API-avain tarvittaessa)
    # API_URL = "https://api.example-3d-converter.com/v1/convert"
    # headers = {"Authorization": "Bearer OMA_API_AVAIN"}
    # files = {'file': open(file_path, 'rb')}
    # response = requests.post(API_URL, headers=headers, files=files)
    
    # MVP-toteutus / Mock-simulaatio kehitystä varten:
    print(f"Käsitellään tiedostoa 3D-malliksi: {file_path}")
    
    # Jos tiedosto on jo .glb, palautetaan se suoraan
    if file_path.endswith(".glb"):
        return file_path
        
    # Simulaatiossa palautetaan tiedoston polku (tuotannossa tähän tulee API:n palauttama .glb-polku)
    return file_path

def convert_floorplan_to_3d(file_path):
    """
    Muuntaa 2D-pohjapiirroksen (esim. PDF tai kuva) tyhjäksi 3D-malliksi (.glb).
    Ekstruudoi seinät automaattisesti, jotta digitaalinen kaksonen ja virtuaalinen 
    stailaus voidaan käynnistää pelkän pohjapiirroksen pohjalta.
    """
    print(f"Muunnetaan 2D-pohjapiirros tyhjäksi 3D-malliksi: {file_path}")
    
    # Tarkistetaan tiedostomuoto
    if file_path.endswith(".glb"):
        return file_path

    # MVP / Simulaatiologiikka: Luodaan mallin polku ja varmistetaan kansio
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_glb_path = os.path.join(UPLOAD_DIR, f"{base_name}_empty_floorplan.glb")
    
    # Simulaatiossa voidaan kopioida tai merkitä tiedosto käsitellyksi
    # Tuotannossa tähän kytketään pohjakuvan AI-ekstruusio-rajapinta
    try:
        shutil.copy(file_path, output_glb_path)
    except Exception:
        pass
        
    return output_glb_path

def process_virtual_staging(file_path, remove_furniture=False):
    """
    Käsittelee ladatun videon tai kuvan: poistaa haluttaessa huonekalut (Virtual Staging)
    tai valmistelee sen puhtaaksi 3D-malliksi.
    """
    if remove_furniture:
        print(f"Suoritetaan tekoälypohjainen huonekalujen poisto kohteelle: {file_path}")
        processed_path = file_path.replace(".", "_empty.")
        try:
            shutil.copy(file_path, processed_path)
            return processed_path
        except Exception:
            return file_path
            
    return file_path
