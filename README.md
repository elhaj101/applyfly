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



new template:

{sender_name}
{sender_address_line1}
{sender_address_line2}
{sender_postal_code} {sender_city}

{recipient_company}
{recipient_address_line1}
{recipient_address_line2}
{recipient_postal_code} {recipient_city}

		{place}, den {date}

Bewerbung als {job_position} (Kennziffer {reference_number})

{salutation}

mit großer Begeisterung bewerbe ich mich als qualifizierte und leidenschaftliche {target_language} {job_title}. Durch mein {education_background} sowie meine langjährige Erfahrung im {experience_area1} und in einem {experience_area2} verfüge ich über das ideale Rüstzeug, um umfassende Fertigkeiten in {skills_list} zu vermitteln.

Aktuell bin ich unter anderem als {current_position} an einem {current_institution} tätig und verfasse parallel dazu meine {thesis_type} in {thesis_topic}. Meine bisherigen Tätigkeiten an einem {previous_institution} beinhalteten unter anderem das Erstellen von {responsibility1} und {responsibility2}. Im Rahmen meiner Lehrtätigkeit in einer {previous_context} habe ich einen {specific_course} mit {target_audience} geleitet. Dabei lag der Fokus auf der selbstständigen Erstellung von {created_materials} sowie der Vermittlung von {taught_skills}.

Während meines Studiums verbrachte ich regelmäßig Zeit {immersion_experience}. Von {internship_start} bis {internship_end} engagierte ich mich {internship_type} bei {organization}. Die Tätigkeiten fanden ausschließlich auf {language} statt, und ich war aktiv an der Entwicklung und Umsetzung von {developed_concepts} beteiligt.

Durch meine Tätigkeiten habe ich meine {soft_skill1} und {soft_skill2} enorm erweitert. Eine effektive Zusammenarbeit im Team war unerlässlich. Darüber hinaus war eine klare und effektive Kommunikation entscheidend für den Erfolg meiner Tätigkeiten.

Mit meiner Leidenschaft für die {language} und meiner umfangreichen Expertise bin ich überzeugt, dass ich eine wertvolle Bereicherung für Ihr Team darstellen kann. Ich freue mich auf Ihre Einladung.

{closing}

{full_name}