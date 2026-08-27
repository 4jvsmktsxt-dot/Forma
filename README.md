# 🏠 Forma - Digitaalinen LKV-hallintapaneeli & Remonttilaskenta

Forma on moderni, tekoälyllä ja reaaliaikaisella analytiikalla varustettu kiinteistöresurssien hallinta- ja myyntialusta. Se yhdistää LKV-välittäjien työtilat, remonttimyyjien lisämyyntityökalut sekä ostajien digitaaliset mikrokyselyt yhdeksi saumattomaksi kokonaisuudeksi.

## 🚀 Keskeiset ominaisuudet

* **🏠 LKV-välittäjän työtila:** Kohteiden hallinta, dynaamiset mittarit, hinnoittelulaskuri ja ostajakyselyt.
* **🔨 Remonttimyyjän työtila:** Ostajien remonttialttuus, liukusäädinmetriikat ja terassi-/pintaremontin lisämyyntipaketit.
* **👑 Master Dashboard & Ingest Hub:** Koko portfolion laaja bisnesanalytiikka, kohteiden lisäys sekä automaattinen sähköpostien (Gmail IMAP) ja mediakuvien tuonti.
* **🤖 AI-asiantuntija-agentit:** Sisustaja-, remontti- ja kauppavalmentaja-agentit, jotka auttavat kuvien ja pohjapiirustusten tulkinnassa.
* **📐 3D-mallikatselin:** Integroitu tuettu tuki interaktiivisille `.glb`-malleille (Google Model-Viewer).

## 🗂️ Järjestelmän rakenne (Moduulit)

* `app.py` – Pääsovellus ja roolipohjainen käyttöliittymä (Streamlit)
* `database.py` – SQLite-tietokantakerros ja taulujen hallinta (`forma_master.db`)
* `agents.py` – Forma AI -asiantuntija-agenttien chat-logiikka
* `buyer_intake.py` – Ostajan mikrokyselylomake (liukusäätimet ja monivalinnat)
* `pricing.py` – Hinnoittelu- ja lisämyyntimoottori (terassit ja toteutumaennusteet)
* `master_dashboard.py` – Liiketoiminnan komentokeskus ja KPI-kortit
* `ingest_hub.py` – Sähköpostien liitteiden automaattihaku (Gmail IMAP)
* `storage.py` – Tiedostojen hallinta, UUID-nimeksemme ja 3D-konversion runko
* `components.py` – 3D-mallien selainkatselin
* `metrics.py` – Dynaamiset kohteiden mittarit ja ostajadatan analytiikka

## ⚙️ Ohjeet käynnistykseen

1. Kloonaa repositorio omalle koneellesi tai avaa se pilviympäristössä.
2. Asenna tarvittavat kirjastot komentoriviltä:

```bash
pip install -r requirements.txt
