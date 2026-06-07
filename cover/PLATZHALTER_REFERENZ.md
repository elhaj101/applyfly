# DIN 5008 Bewerbungsschreiben — Platzhalter-Referenz

## Vorlagendatei: `din5008_bewerbung_vorlage.docx`

Alle Platzhalter sind im Format `{{PLATZHALTER_NAME}}` in blauer unterstrichener Schrift dargestellt.

---

## Platzhalter-Übersicht

| Platzhalter | Beschreibung | Beispiel |
|---|---|---|
| `{{ABSENDER_NAME}}` | Vollständiger Name des Absenders | `Maassouma Kristina Dabbous` |
| `{{ABSENDER_STRASSE}}` | Straße und Hausnummer des Absenders | `Seestr. 30` |
| `{{ABSENDER_PLZ_ORT}}` | PLZ und Ort des Absenders | `13353 Berlin` |
| `{{ABSENDER_TELEFON}}` | Telefonnummer des Absenders | `0176 4534 4885` |
| `{{ABSENDER_EMAIL}}` | E-Mail-Adresse des Absenders | `maassouma1@yahoo.de` |
| `{{EMPFAENGER_FIRMA}}` | Firma oder Behörde des Empfängers | `Bundesnachrichtendienst (BND)` |
| `{{EMPFAENGER_ABTEILUNG}}` | Abteilung oder Postfach | `Postfach 08 01 54` |
| `{{EMPFAENGER_STRASSE}}` | Straße und Hausnummer des Empfängers | *(leer lassen bei Postfach)* |
| `{{EMPFAENGER_PLZ_ORT}}` | PLZ und Ort des Empfängers | `10001 Berlin` |
| `{{ORT}}` | Ort für die Datumszeile | `Berlin` |
| `{{DATUM}}` | Datum des Schreibens | `22.04.2024` |
| `{{BETREFF}}` | Betreffzeile (fett) | `Bewerbung als Sprachlehrer/in für Arabisch (Kennziffer ID/031-15)` |
| `{{ANREDE}}` | Anrede | `Sehr geehrte Damen und Herren,` |
| `{{EINLEITUNGSSATZ}}` | Erster Absatz / Einstiegssatz | *(vollständiger Absatz)* |
| `{{HAUPTTEIL_ABSATZ_1}}` | Hauptteil Absatz 1 | *(vollständiger Absatz)* |
| `{{HAUPTTEIL_ABSATZ_2}}` | Hauptteil Absatz 2 | *(vollständiger Absatz)* |
| `{{HAUPTTEIL_ABSATZ_3}}` | Hauptteil Absatz 3 (optional) | *(kann leer bleiben)* |
| `{{SCHLUSSSATZ}}` | Schlusssatz | `Ich freue mich auf Ihre Einladung.` |
| `{{GRUSSFORMEL}}` | Grußformel | `Mit freundlichen Grüßen,` |
| `{{ABSENDER_VOLLNAME}}` | Name unter der Unterschrift | `Maassouma Dabbous` |
| `{{ANLAGEN}}` | Anlagenangaben (optional) | `Lebenslauf, Zeugnisse` |

---

## DIN 5008 Formatierungsrichtlinien

Die Vorlage und der Generator richten sich nach den offiziellen Empfehlungen der DIN 5008 (Form B) für Geschäftsbriefe und Bewerbungen. 

### 1. Seitenränder
- **Oben:** 45 mm (4,5 cm) - *Bietet Platz für den Briefkopf und das Anschriftenfeld (Form B).*
- **Unten:** 20 mm (2,0 cm)
- **Links:** 25 mm (2,5 cm) - *Sorgt für ausreichend Platz zum Abheften.*
- **Rechts:** 20 mm (2,0 cm)

### 2. Zeilenabstand & Ausrichtung
- **Zeilenabstand:** Der Standard ist **1,15** (oder einfacher Zeilenabstand 1,0). Dies sorgt für optimale Lesbarkeit. Der Generator erzwingt automatisch einen Zeilenabstand von 1,15 für das gesamte Dokument.
- **Textausrichtung:** Das gesamte Anschreiben wird **linksbündig** (Flattersatz) formatiert. Blocksatz ist laut DIN 5008 nicht empfohlen, da er bei Standard-Schriftarten oft zu unregelmäßigen Wortabständen führt.

### 3. Schriftart & Schriftgröße
- **Schriftart:** Serifenlose Schriften wie *Arial*, *Calibri* oder *Helvetica* werden bevorzugt. Auch klassische Serifenschriften wie *Times New Roman* sind zulässig.
- **Schriftgröße (Fließtext):** 11 pt oder 12 pt.
- **Schriftgröße (Kontaktangaben/Fußzeile):** 10 pt.

### 4. Layout-Struktur & Abstände (Leerzeilen)
Das Dokument ist strukturell wie folgt aufgebaut:
- **Absender:** Oben rechts oder im Briefkopf (oben links).
- **Empfänger:** Linksbündig. Beginnt ca. 4,5 cm vom oberen Rand.
- **Ort & Datum:** Rechtsbündig (z.B. `Berlin, den 15.08.2026`).
- **Betreff:** Linksbündig und **fett** gedruckt. Es folgen **zwei Leerzeilen** bis zur Anrede.
- **Anrede:** Linksbündig. Danach folgt **eine Leerzeile**.
- **Brieftext (Body):** Die Absätze (Einleitung, Hauptteile, Schlusssatz) werden jeweils durch **eine Leerzeile** voneinander getrennt.
- **Grußformel:** Linksbündig. Danach folgen **drei Leerzeilen** für die handschriftliche Unterschrift.
- **Anlagen:** Linksbündig unter dem vollständigen Namen.

---

## Streamlit — Python-Ersetzungslogik

```python
from docx import Document
import io

def vorlage_befuellen(vorlagen_pfad: str, daten: dict) -> bytes:
    """
    Lädt die DIN-5008-Vorlage und ersetzt alle {{PLATZHALTER}}-Tokens.

    Args:
        vorlagen_pfad: Pfad zur din5008_bewerbung_vorlage.docx
        daten: Dict mit Platzhalter-Schlüsseln und Ersetzungswerten
               z.B. {"ABSENDER_NAME": "Max Mustermann", "ORT": "Berlin", ...}

    Returns:
        Ausgefüllte DOCX-Datei als Bytes (direkt für st.download_button nutzbar)
    """
    dok = Document(vorlagen_pfad)

    def in_absatz_ersetzen(absatz, daten):
        for run in absatz.runs:
            for schluessel, wert in daten.items():
                platzhalter = f"{{{{{schluessel}}}}}"
                if platzhalter in run.text:
                    run.text = run.text.replace(platzhalter, wert)
                    # Formatierung zurücksetzen: Blau und Unterstreichung entfernen
                    run.font.color.rgb = None
                    run.font.underline = False

    for absatz in dok.paragraphs:
        in_absatz_ersetzen(absatz, daten)

    puffer = io.BytesIO()
    dok.save(puffer)
    puffer.seek(0)
    return puffer.getvalue()


# ── Streamlit-App Beispiel ────────────────────────────────────────────────────

import streamlit as st

st.title("DIN 5008 Bewerbungsschreiben Generator")

with st.form("brief_formular"):
    st.subheader("Absender")
    absender_name    = st.text_input("Vollständiger Name", "Max Mustermann")
    absender_strasse = st.text_input("Straße & Hausnummer", "Musterstraße 1")
    absender_plz     = st.text_input("PLZ & Ort", "10115 Berlin")
    absender_tel     = st.text_input("Telefon", "0176 1234 5678")
    absender_email   = st.text_input("E-Mail", "max@example.de")

    st.subheader("Empfänger")
    empf_firma    = st.text_input("Firma / Behörde", "Muster GmbH")
    empf_abt      = st.text_input("Abteilung / Postfach", "Personalabteilung")
    empf_strasse  = st.text_input("Straße (leer = kein Eintrag)", "")
    empf_plz      = st.text_input("PLZ & Ort", "80331 München")

    st.subheader("Datum & Betreff")
    ort     = st.text_input("Ort", "Berlin")
    datum   = st.text_input("Datum", "01.01.2024")
    betreff = st.text_input("Betreff", "Bewerbung als ... (Kennziffer ...)")

    st.subheader("Briefinhalt")
    anrede      = st.text_input("Anrede", "Sehr geehrte Damen und Herren,")
    einleitung  = st.text_area("Einleitungssatz (Absatz 1)")
    absatz1     = st.text_area("Hauptteil Absatz 1")
    absatz2     = st.text_area("Hauptteil Absatz 2")
    absatz3     = st.text_area("Hauptteil Absatz 3 (optional)", "")
    schlusssatz = st.text_input("Schlusssatz", "Ich freue mich auf Ihre Einladung.")
    grussformel = st.text_input("Grußformel", "Mit freundlichen Grüßen,")
    anlagen     = st.text_input("Anlagen", "Lebenslauf, Zeugnisse")

    abgeschickt = st.form_submit_button("Brief erstellen")

if abgeschickt:
    daten = {
        "ABSENDER_NAME":        absender_name,
        "ABSENDER_STRASSE":     absender_strasse,
        "ABSENDER_PLZ_ORT":     absender_plz,
        "ABSENDER_TELEFON":     absender_tel,
        "ABSENDER_EMAIL":       absender_email,
        "EMPFAENGER_FIRMA":     empf_firma,
        "EMPFAENGER_ABTEILUNG": empf_abt,
        "EMPFAENGER_STRASSE":   empf_strasse,
        "EMPFAENGER_PLZ_ORT":   empf_plz,
        "ORT":                  ort,
        "DATUM":                datum,
        "BETREFF":              betreff,
        "ANREDE":               anrede,
        "EINLEITUNGSSATZ":      einleitung,
        "HAUPTTEIL_ABSATZ_1":   absatz1,
        "HAUPTTEIL_ABSATZ_2":   absatz2,
        "HAUPTTEIL_ABSATZ_3":   absatz3,
        "SCHLUSSSATZ":          schlusssatz,
        "GRUSSFORMEL":          grussformel,
        "ABSENDER_VOLLNAME":    absender_name,
        "ANLAGEN":              anlagen,
    }

    docx_bytes = vorlage_befuellen("din5008_bewerbung_vorlage.docx", daten)

    st.download_button(
        label="📄 Brief als .docx herunterladen",
        data=docx_bytes,
        file_name=f"Bewerbung_{absender_name.replace(' ', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
```

---

## Hinweise

- **Optionale Platzhalter** (`{{EMPFAENGER_STRASSE}}`, `{{HAUPTTEIL_ABSATZ_3}}`, `{{ANLAGEN}}`): Bei leerem Wert wird der Platzhalter einfach gelöscht. Soll der gesamte Absatz entfernt werden, kann der Absatz in Python geprüft und gelöscht werden.
- **Zeichenkodierung**: Vollständige UTF-8-Unterstützung — Umlaute (ä, ö, ü, ß) funktionieren problemlos.
- **python-docx Version**: Getestet mit `python-docx >= 1.1.0`.
