<div align="center">

# ✈️ applyfly

**Privacy-First German Cover Letter Generator — DIN 5008 Compliant**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

Generate perfectly formatted German cover letters (Anschreiben) that comply with the official **DIN 5008** standard — directly in your browser, with all data stored locally on your machine.

</div>

---

## ✨ Features

- 📄 **DIN 5008 Compliant** — Correct margins, spacing, layout and font as per the official German business letter standard (Form B)
- 🔒 **Privacy First** — All data is stored in a local SQLite database. Nothing leaves your machine
- 🔑 **Field Locking** — Click the 🔒 icon next to any field to save it across sessions (great for your salutation, valediction, or frequently used recipients)
- 👤 **Sender Profiles** — Save multiple sender profiles (e.g. different email addresses or addresses) and load them with one click
- 🖋️ **Font Selection** — Choose between **Arial** or **Times New Roman** for the generated document
- 📦 **One-Page Enforced** — Built-in character limits per paragraph keep your letter on a single page
- 📱 **Responsive UI** — Works on mobile phones and desktop browsers

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/elhaj101/applyfly.git
cd applyfly
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
applyfly/
├── app.py                  # Main Streamlit application
├── database.py             # SQLite database logic (users, profiles, locked fields)
├── requirements.txt        # Python dependencies
├── cover/
│   ├── din5008_bewerbung_vorlage.docx  # DIN 5008 Word template
│   └── PLATZHALTER_REFERENZ.md         # Placeholder reference & formatting standards
└── README.md
```

---

## 📐 DIN 5008 Standards Applied

The generated `.docx` file strictly follows the official DIN 5008 (Form B) recommendations:

| Property | Value |
|---|---|
| Top Margin | 35 mm |
| Bottom Margin | 20 mm |
| Left Margin | 25 mm |
| Right Margin | 20 mm |
| Font Size (body) | 11 pt |
| Line Spacing | 1.15 |
| Text Alignment | Left-aligned (Flattersatz) |
| Date Position | Right-aligned |
| Subject Line | Bold, left-aligned |

---

## 🔒 The Lock System

Every lockable input field has a 🔒 icon next to it:

- **Grey (🔒 dimmed)** = field is not locked, value is entered fresh each time
- **Coloured (🔒 bright)** = field is locked — the current value is saved to your local database and will be **auto-filled on your next login**

Click the icon once to toggle. No page reload, no data leaves your device.

---

## 📝 How to Use

1. **Sign Up / Log In** — Create a local account (stored only on your device)
2. **Create a Sender Profile** — Go to the "Manage Profiles" tab and save your personal details
3. **Generate a Cover Letter** — In the "Generate Document" tab:
   - Select your sender profile
   - Fill in recipient details
   - Choose your font
   - Write your letter in the structured paragraph boxes
   - Click **Generate Document** and download the `.docx` file
4. **Export to PDF** — Open the downloaded file in Apple Pages or Word and export as PDF before sending

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [python-docx](https://python-docx.readthedocs.io) | Word document generation |
| [SQLite](https://sqlite.org) + [Werkzeug](https://werkzeug.palletsprojects.com) | Local database & password hashing |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

MIT License — feel free to use, modify, and distribute.

---

<div align="center">
Made with ❤️ for the German job market
</div>