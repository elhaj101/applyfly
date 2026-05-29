# applyfly - Secure Document Formatter

## System Architecture
applyfly is a privacy-first web application built with a pure Python, zero-cloud architecture. It uses **Streamlit** for the frontend user interface, a **local SQLite** database (`applyfly_local.db`) for secure data persistence and user authentication, and in-memory rendering (`io.BytesIO`) to generate the document without leaving traces on the disk. This ensures maximum data privacy: no user data, profile information, or generated `.docx` documents are ever sent to external cloud servers. 

## Implementation Roadmap (Step-by-Step)

1. **Environment Initialization:**
   Set up your project environment by installing the required dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

2. **Template Construction:**
   You must manually create a Word document named `din_5008_template.docx` in the root directory.
   - Set the page margins in Word to adhere to the DIN 5008 standard (Left: 2.5cm, Top: 4.5cm).
   - Paste the following exact Jinja2 tags into the document layout where appropriate:
     - `{{ sender_name }}`
     - `{{ sender_street }}`
     - `{{ sender_city_zip }}`
     - `{{ sender_phone }}`
     - `{{ sender_email }}`
     - `{{ recipient_company }}`
     - `{{ recipient_department }}`
     - `{{ recipient_street }}`
     - `{{ recipient_city_zip }}`
     - `{{ date }}`
     - `{{ job_title }}`
     - `{{ salutation }}`
     - `{{ cover_letter_body }}`

3. **Database Generation:**
   The local database file (`applyfly_local.db`) will auto-generate upon the first run of the application. It creates all necessary tables for users and sender profiles automatically.

4. **Execution:**
   Start the local server using Streamlit to launch the app:
   ```bash
   streamlit run app.py
   ```

## Deployment Checklist

- [ ] Installing dependencies (`pip install -r requirements.txt`)
- [ ] Manually building and placing the master `din_5008_template.docx` template in the project root
- [ ] Testing the sign-up and password hashing flow
- [ ] Creating a test sender profile
- [ ] Verifying paragraph spacing works in the generated `.docx` output