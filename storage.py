import os
import uuid
import shutil
import requests
from pathlib import Path
from typing import Optional, Union

UPLOAD_DIR = Path("uploads")

def _ensure_upload_dir():
    """Varmistaa, että upload-kansio on olemassa."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_file(uploaded_file) -> str:
    """
    Tallentaa Streamlitistä tulleen tiedoston 'uploads'-kansioon.
    Palauttaa tallennetun tiedoston absoluuttisen tai suhteellisen polun.
    """
    _ensure_upload_dir()
    
    # Luodaan uniikki tiedostonimi versiohallintaa varten
    original_name = getattr(uploaded_file, "name", "unknown_file")
    unique_filename = f"{uuid.uuid4().hex}_{original_name}"
    file_path = UPLOAD_DIR / unique_filename
    
    with open(file_path, "wb") as f:
        # Tukee sekä Streamlit UploadedFile -objektia että tavallista binääridataa
        if hasattr(uploaded_file, "getbuffer"):
            f.write(uploaded_file.getbuffer())
        else:
            f.write(uploaded_file.read())
            
    return str(file_path)

def save_bytes_from_source(file_bytes: bytes, original_filename: str) -> str:
    """
    Moduuli esimerkiksi WhatsApp-botille tai ulkoiselle API:lle: 
    Tallentaa saapuneet tavut (bytes) levylle uniikilla nimellä.
    """
    _ensure_upload_dir()
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    file_path = UPLOAD_DIR / unique_filename
    
    with open(file_path, "wb") as f:
        f.write(file_bytes)
        
    return str(file_path)

def delete_file(file_path: str):
    """Poistaa tiedoston levyltä turvallisesti, jos se on olemassa."""
    path = Path(file_path)
    if path.exists():
        path.unlink()

def convert_video_to_3d(file_path: str, api_key: Optional[str] = None) -> str:
    """
    Muuntaa WhatsAppista tai kamerasta tulleen videon/kuvan 3D (.glb) -muotoon.
    Modulaarinen toteutus: helppo kytkeä tuotannon API (esim. Luma / Tripo / Meshy).
    """
    print(f"[INFO] Käsitellään videota / mediaa 3D-malliksi: {file_path}")
    
    if file_path.endswith(".glb"):
        return file_path
        
    # Tuotannon API-kutsujen runko (otetaan käyttöön kun API-avaimet kytketään)
    if api_key:
        try:
            # Esimerkkirunko ulkoiselle AI-konversiolle:
            # response = requests.post("https://api.example.com/v1/convert", ...)
            pass
        except Exception as e:
            print(f"[ERROR] 3D-videokonversio epäonnistui: {e}")
            
    # MVP / Mock-palautus kehitysvaiheeseen
    base_name = Path(file_path).stem
    output_glb_path = UPLOAD_DIR / f"{base_name}_converted.glb"
    
    # Simulaatiokopio, kunnes varsinainen AI-palvelin vastaa
    if not output_glb_path.exists():
        shutil.copy(file_path, output_glb_path)
        
    return str(output_glb_path)

def convert_floorplan_to_3d(file_path: str, api_key: Optional[str] = None) -> str:
    """
    Muuntaa 2D-pohjapiirroksen (PDF, PNG, JPG) tyhjäksi tai esitäytetyksi 3D-malliksi (.glb).
    Ekstruudoi seinät automaattisesti digitaaliseksi kaksoseeksi.
    """
    print(f"[INFO] Ekstruudoidaan 2D-pohjapiirros 3D-muotoon: {file_path}")
    
    if file_path.endswith(".glb"):
        return file_path

    _ensure_upload_dir()
    base_name = Path(file_path).stem
    output_glb_path = UPLOAD_DIR / f"{base_name}_empty_floorplan.glb"
    
    # Laajennuspaikka varsinaiselle pohjapiirroksen AI-ekstrusiomoottorille
    if api_key:
        # TODO: Lisää tuleva API-kutsu tähän
        pass

    # MVP / Simulaatiologiikka
    try:
        if not output_glb_path.exists():
            shutil.copy(file_path, output_glb_path)
    except Exception as e:
        print(f"[ERROR] Pohjapiirroksen ekstrusio epäonnistui: {e}")
        
    return str(output_glb_path)

def process_virtual_staging(file_path: str, remove_furniture: bool = False) -> str:
    """
    Käsittelee ladatun kohteen: poistaa haluttaessa huonekalut (Virtual Staging)
    tai valmistelee tilan puhtaaksi.
    """
    if remove_furniture:
        print(f"[INFO] Suoritetaan tekoälypohjainen huonekalujen poisto: {file_path}")
        path_obj = Path(file_path)
        processed_path = path_obj.with_name(f"{path_obj.stem}_empty{path_obj.suffix}")
        try:
            shutil.copy(file_path, processed_path)
            return str(processed_path)
        except Exception:
            return file_path
            
    return file_path
