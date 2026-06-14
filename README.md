<div align="center">

# ✈️ applyfly

**German Cover Letter Generator — DIN 5008 Compliant**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Postgres](https://img.shields.io/badge/Supabase-Postgres-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

Generate perfectly formatted German cover letters (Anschreiben) that comply with the official **DIN 5008** standard — directly in your browser. User accounts, sender profiles, drawn signatures, and locked fields are persisted in a hosted PostgreSQL database so they survive across devices and sessions.

</div>

---

## ✨ Features

- 📄 **DIN 5008 Compliant** — Correct margins, spacing, layout and font as per the official German business letter standard (Form B)
- 👤 **User Accounts** — Sign up / log in with email + password (passwords hashed with Werkzeug; emails normalised to avoid case/whitespace mismatches)
- 💾 **Sender Profiles** — Save multiple sender profiles (name, address, phone, email, signature) and load them with one click
- 🖋️ **Drawn Signatures** — Sign with your finger (mobile) or mouse (desktop) on a custom canvas pad; the signature is stored on the profile and embedded into the generated document
- 🔒 **Field Locking** — Click the 🔒 icon next to any field to persist its value to your account; locked values are restored after refresh and re-login, and edits to a locked field are saved automatically
- 📝 **Single Body Field** — One free-form "Cover Letter Body" box (blank lines split it into the template's paragraphs) instead of rigid fixed paragraphs
- 🔤 **Font Selection** — Choose between **Arial** or **Times New Roman** for the generated document
- 📦 **One-Page Friendly** — Per-field character limits help keep the letter on a single page; empty optional placeholders are removed from the document
- 📱 **Responsive UI** — Works on mobile phones and desktop browsers
- 🧹 **No Autofill Noise** — Browser autofill/autocorrect is disabled on all inputs (it was firing reruns and causing errors); the UI no longer dims/fades during reruns

---

## 🏗️ Architecture

```
Browser ──▶ Streamlit app (app.py)
                │
                ├── python-docx  ──▶ fills cover/din5008_bewerbung_vorlage.docx
                │
                ├── custom component (components/signature_pad) ──▶ HTML5 canvas signature
                │
                └── database.py ──▶ pooled psycopg2 ──▶ Supabase PostgreSQL
```

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [python-docx](https://python-docx.readthedocs.io) | Word document generation |
| [Supabase](https://supabase.com) PostgreSQL | Persistent storage (users, profiles, locked fields) |
| [psycopg2](https://www.psycopg.org/) | Postgres driver + `ThreadedConnectionPool` |
| [Werkzeug](https://werkzeug.palletsprojects.com) | Password hashing (`generate_password_hash` / `check_password_hash`) |
| Custom Streamlit component (vanilla JS/HTML5 canvas) | Touch-friendly signature pad |

> **Note on storage:** earlier versions used a local SQLite file. That does **not** work on Streamlit Cloud, whose filesystem is ephemeral — the database was wiped on every reboot/redeploy/sleep, which caused signup failures and data loss. Storage was migrated to a hosted PostgreSQL database (Supabase) to make data durable.

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.10+
- A PostgreSQL database (a free [Supabase](https://supabase.com) project works well)

### 1. Clone & install

```bash
git clone https://github.com/elhaj101/applyfly.git
cd applyfly
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure the database connection

Create `.streamlit/secrets.toml` (this file is git-ignored — never commit it):

```toml
DATABASE_URL = "postgresql://postgres.<project-ref>:<password>@<host>.pooler.supabase.com:6543/postgres"
```

Use the Supabase **Connection Pooling** string (Transaction pooler, port **6543**), found via the green **Connect** button in the Supabase dashboard. The app also reads `DATABASE_URL` from the environment if no secret is present (handy for scripts/tests).

### 3. Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`. Tables are created automatically on first launch (`init_db()`).

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push the repo to GitHub (Streamlit Cloud auto-redeploys the tracked branch — usually `main`).
2. In **Manage app → Settings → Secrets**, add the same `DATABASE_URL` line as above.
3. Saving the secret reboots the app; on first load it creates its tables.

A redeploy that changes `requirements.txt` reinstalls dependencies (~2–3 min).

---

## 🗄️ Database Schema

All tables are created idempotently in `init_db()` (with `CREATE TABLE IF NOT EXISTS` and an `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` migration for `signature`).

**`users`**

| Column | Type | Notes |
|---|---|---|
| `id` | SERIAL PK | |
| `email` | TEXT UNIQUE | stored lowercased/trimmed |
| `first_name` | TEXT | |
| `last_name` | TEXT | |
| `password_hash` | TEXT | Werkzeug hash |

**`sender_profiles`**

| Column | Type | Notes |
|---|---|---|
| `id` | SERIAL PK | |
| `user_email` | TEXT | owner |
| `profile_name`, `name`, `street`, `phone`, `email`, `city`, `zip_code` | TEXT | profile fields |
| `signature` | TEXT | base64-encoded PNG of the drawn signature (empty if none) |

**`user_locked_fields`**

| Column | Type | Notes |
|---|---|---|
| `user_email` | TEXT | part of composite PK |
| `field_key` | TEXT | part of composite PK |
| `field_value` | TEXT | persisted value; upserted via `ON CONFLICT ... DO UPDATE` |

### Connection pooling

`database.py` keeps a single `psycopg2.pool.ThreadedConnectionPool` cached with `@st.cache_resource`, so connections are reused across reruns and sessions instead of opening a new TCP+TLS handshake on every query. All queries go through a `_cursor()` context manager that handles commit/rollback and returns the connection to the pool. This eliminated the post-login lag that was caused by multiple fresh connections per render.

---

## 📐 DIN 5008 Standards Applied

The generated `.docx` follows the official DIN 5008 (Form B) recommendations:

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

Placeholders in the template (e.g. `{{ABSENDER_NAME}}`, `{{EMPFAENGER_FIRMA}}`, `{{HAUPTTEIL_ABSATZ_1}}`) are replaced at generation time. Paragraphs whose only content is an **empty** optional placeholder are removed so the letter stays clean. See `cover/PLATZHALTER_REFERENZ.md` for the full placeholder reference.

### Body field mapping

The single **Cover Letter Body** input is split on blank lines into up to three chunks, mapped to `HAUPTTEIL_ABSATZ_1/2/3`. Any text beyond three paragraphs is appended to the third.

### Signature embedding

If the selected profile has a signature, the base64 PNG is decoded and inserted as its own paragraph **directly above** `{{ABSENDER_VOLLNAME}}` using a small `_insert_paragraph_before()` helper. The signature paragraph uses tight spacing (`space_before`/`space_after = Pt(0)`, line spacing `1.0`) and the image is sized to **38 mm** wide. Both the size and spacing are easy to tweak in `vorlage_befuellen()` in `app.py`.

---

## 🖋️ The Signature Pad

Rather than a third-party canvas (which had poor mobile touch support), applyfly ships a small **custom Streamlit component** at `components/signature_pad/index.html`:

- Vanilla HTML5 `<canvas>` with native `mouse*` and `touch*` handlers (`touch-action: none`) so it works on phones and desktops alike.
- **Draw** button activates the pad, **Clear** resets, **OK** confirms — confirmation returns a `data:image/png;base64,...` URL to Python via the Streamlit component message protocol (`setComponentValue`).
- The app strips the data-URL prefix and stores the base64 PNG on the profile. A versioned widget key resets the pad after each save so a new profile starts blank.

---

## 🔒 The Lock System

Every lockable input has a 🔒 icon next to it:

- **Grey (dimmed)** = not locked; value entered fresh each time
- **Coloured (bright)** = locked; the value is saved to your account and **restored on your next login**

Toggling the lock saves/deletes the value immediately (no reload). While a field is locked, **editing it re-saves automatically**, so the latest value always persists. Logging out clears the session so the next user starts clean.

---

## 📝 How to Use

1. **Sign Up / Log In** — create an account (email + password)
2. **Create a Sender Profile** — in **Manage Profiles**, fill your details and optionally draw a signature (Draw → sign → OK), then **Save Profile**
3. **Generate a Cover Letter** — in **Generate Document**:
   - Select your sender profile (its signature is embedded automatically)
   - Fill in recipient details
   - Choose your font
   - Write your letter in the single **Cover Letter Body** box (blank lines = new paragraphs)
   - Click **Generate Document** and download the `.docx`
4. **Export to PDF** — open the `.docx` in Word / Apple Pages and export as PDF before sending

---

## 📁 Project Structure

```
applyfly/
├── app.py                              # Main Streamlit app (UI, docx generation, signature embedding)
├── database.py                         # Postgres logic: pooled connections, users, profiles, locked fields
├── requirements.txt                    # Python dependencies
├── components/
│   └── signature_pad/
│       └── index.html                  # Custom HTML5 canvas signature component
├── cover/
│   ├── din5008_bewerbung_vorlage.docx  # DIN 5008 Word template
│   └── PLATZHALTER_REFERENZ.md         # Placeholder reference & formatting standards
├── .streamlit/
│   └── secrets.toml                    # DATABASE_URL (git-ignored — create locally)
└── README.md
```

---

## 🔐 Security Notes

- `DATABASE_URL` (which contains the DB password) belongs **only** in `.streamlit/secrets.toml` (git-ignored) or the Streamlit Cloud Secrets box — never in a tracked file.
- Rotate the Supabase database password if it has ever been shared/exposed (Supabase → Settings → Database → Reset database password), then update the secret in both local and cloud configs.
- Passwords are stored only as Werkzeug hashes; plaintext passwords are never persisted.

---

## 🧰 Technical Changelog (Highlights)

- **Storage migration:** local SQLite → Supabase PostgreSQL (`psycopg2`), fixing signup failures and data loss on Streamlit Cloud's ephemeral filesystem.
- **Auth hardening:** email normalisation (trim + lowercase) and basic format validation on signup/login.
- **Lock persistence:** locked-field edits now save immediately; session state is cleared on logout so locks don't leak between users.
- **Single body field:** replaced three fixed paragraph inputs with one free-form body, split on blank lines into template paragraphs.
- **Drawable signature:** custom touch-friendly HTML5 canvas component; signature stored per profile (base64 PNG) and embedded into the `.docx` above the sender name (38 mm wide, tight spacing).
- **Performance:** cached `ThreadedConnectionPool`, once-per-session `init_db`, and de-duplicated profile queries — removed the post-login render lag.
- **UX polish:** disabled browser autofill/autocorrect on all inputs; suppressed the rerun fade/dim; the word **applyfly** is shown in red on both the login and dashboard titles.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📜 License

MIT License — feel free to use, modify, and distribute.

---

<div align="center">
Made with ❤️ for the German job market
</div>
