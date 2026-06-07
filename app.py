import streamlit as st
import datetime
import io
import os
from docx import Document
from docx.shared import Mm
from docx.enum.text import WD_LINE_SPACING
from database import init_db, create_user, verify_user, save_profile, get_all_profiles, delete_profile, save_locked_field, get_locked_fields, delete_locked_field

def vorlage_befuellen(vorlagen_pfad: str, daten: dict, selected_font: str = "Arial") -> bytes:
    dok = Document(vorlagen_pfad)

    # Enforce margins
    for section in dok.sections:
        section.top_margin = Mm(35)
        section.bottom_margin = Mm(20)
        section.left_margin = Mm(25)
        section.right_margin = Mm(20)

    # Optional paragraph removal: remove any paragraph that only contains an empty placeholder
    placeholders_to_check = [
        'EMPFAENGER_FIRMA', 'EMPFAENGER_ABTEILUNG', 'EMPFAENGER_STRASSE', 'EMPFAENGER_PLZ', 'EMPFAENGER_ORT',
        'EINLEITUNGSSATZ', 'HAUPTTEIL_ABSATZ_1', 'HAUPTTEIL_ABSATZ_2', 'HAUPTTEIL_ABSATZ_3'
    ]
    for p in list(dok.paragraphs):
        text = p.text
        for ph in placeholders_to_check:
            ph_token = f"{{{{{ph}}}}}"
            if ph_token in text and not daten.get(ph, '').strip():
                p._element.getparent().remove(p._element)
                break

    def in_absatz_ersetzen(absatz, daten):
        for run in absatz.runs:
            for schluessel, wert in daten.items():
                platzhalter = f"{{{{{schluessel}}}}}"
                if platzhalter in run.text:
                    run.text = run.text.replace(platzhalter, wert)
                    run.font.color.rgb = None
                    run.font.underline = False
            # Override font for all runs
            run.font.name = selected_font

    for absatz in dok.paragraphs:
        in_absatz_ersetzen(absatz, daten)

    puffer = io.BytesIO()
    dok.save(puffer)
    puffer.seek(0)
    return puffer.getvalue()

# Initialize DB on start
init_db()

st.set_page_config(page_title="applyfly", page_icon="📄", layout="wide")

st.markdown("""
<style>
/* --- Responsive layout --- */
@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    div[data-testid="stColumn"] { min-width: 100% !important; }
}

/* --- Lock toggle: hide the checkbox square entirely --- */
div[data-testid="stCheckbox"] [data-baseweb="checkbox"] > div:first-child {
    display: none !important;
}
/* Remove extra left padding from hidden box */
div[data-testid="stCheckbox"] label[data-baseweb="checkbox"] {
    padding-left: 0 !important;
    gap: 0 !important;
}
/* Unchecked → grey, small font */
div[data-testid="stCheckbox"] {
    filter: grayscale(100%);
    opacity: 0.35;
    transition: filter 0.15s ease, opacity 0.15s ease;
    cursor: pointer;
    font-size: 1.2rem;
    line-height: 1;
}
/* Checked → full colour */
div[data-testid="stCheckbox"]:has(input:checked) {
    filter: none;
    opacity: 1;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

def login_flow():
    st.title("Welcome to applyfly")
    st.subheader("Your Privacy-First German Cover Letter Formatter")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.markdown("### Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if verify_user(login_email, login_password):
                st.session_state.logged_in = True
                st.session_state.user_email = login_email
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid email or password.")
                
    with tab2:
        st.markdown("### Sign Up")
        signup_first_name = st.text_input("First Name")
        signup_last_name = st.text_input("Last Name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_password_confirm = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if signup_password != signup_password_confirm:
                st.error("Passwords do not match.")
            elif not signup_email or not signup_first_name or not signup_last_name or not signup_password:
                st.error("Please fill in all fields.")
            else:
                if create_user(signup_email, signup_first_name, signup_last_name, signup_password):
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.error("Email already exists.")

if not st.session_state.logged_in:
    login_flow()
else:
    # Main Dashboard Sidebar
    st.sidebar.title(f"Hello, {st.session_state.user_email.split('@')[0]}!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()
        
    st.title("applyfly Dashboard")
    
    tab_gen, tab_prof = st.tabs(["📄 Generate Document", "💾 Manage Profiles"])
    
    with tab_prof:
        st.header("Manage Sender Profiles")
        
        # Create new profile
        with st.expander("Create New Profile"):
            new_profile_name = st.text_input("Profile Name (e.g., 'Software Dev Profile')")
            new_name = st.text_input("Full Name")
            new_street = st.text_input("Street Address")
            new_zip = st.text_input("ZIP Code")
            new_city = st.text_input("City")
            new_phone = st.text_input("Phone Number")
            new_email = st.text_input("Email Address")
            
            if st.button("Save Profile"):
                if new_profile_name and new_name and new_street and new_zip and new_city and new_phone and new_email:
                    save_profile(st.session_state.user_email, new_profile_name, new_name, new_street, new_phone, new_email, new_city, new_zip)
                    st.success("Profile saved successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")
                    
        # List and delete profiles
        st.subheader("Saved Profiles")
        profiles = get_all_profiles(st.session_state.user_email)
        if not profiles:
            st.info("No saved profiles found.")
        else:
            for p in profiles:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{p['profile_name']}** ({p['name']} - {p['email']})")
                with col2:
                    if st.button("Delete", key=f"del_{p['id']}"):
                        delete_profile(p['id'], st.session_state.user_email)
                        st.rerun()
                        
    with tab_gen:
        st.header("Generate Cover Letter")
        
        selected_font = st.selectbox("Select Document Font", ["Arial", "Times New Roman"])
        
        # Seed session_state locks from DB only once per login session
        if "locks" not in st.session_state:
            st.session_state.locks = get_locked_fields(st.session_state.user_email)
        locked_fields = st.session_state.locks
        
        def render_locked_input(label, key, default_val="", is_textarea=False, **kwargs):
            col_lock, col_input = st.columns([1, 11])
            locked = key in locked_fields
            
            with col_input:
                # Show locked value if available, otherwise default
                val = locked_fields.get(key, default_val)
                input_key = f"input_{key}"
                if is_textarea:
                    input_val = st.text_area(label, value=val, key=input_key, **kwargs)
                else:
                    input_val = st.text_input(label, value=val, key=input_key, **kwargs)
            
            with col_lock:
                st.write("")
                st.write("")
                # on_change callback fires immediately when toggled — no rerun needed
                def _on_toggle(k=key, get_val=lambda: st.session_state.get(f"input_{key}", default_val)):
                    new_state = st.session_state[f"check_lock_{k}"]
                    current_val = st.session_state.get(f"input_{k}", default_val)
                    if new_state:
                        save_locked_field(st.session_state.user_email, k, current_val)
                        st.session_state.locks[k] = current_val
                    else:
                        delete_locked_field(st.session_state.user_email, k)
                        st.session_state.locks.pop(k, None)
                
                st.checkbox(
                    "🔒",
                    value=locked,
                    key=f"check_lock_{key}",
                    on_change=_on_toggle,
                )
                    
            return input_val
        
        profiles = get_all_profiles(st.session_state.user_email)
        profile_options = {p['profile_name']: p for p in profiles}
        
        selected_profile_name = st.selectbox("Select Sender Profile", options=["-- Select a Profile --"] + list(profile_options.keys()))
        
        selected_profile = profile_options.get(selected_profile_name, {}) if selected_profile_name != "-- Select a Profile --" else {}
        
        st.subheader("Sender Information")
        col1, col2 = st.columns(2)
        with col1:
            sender_name = st.text_input("Sender Name", value=selected_profile.get('name', ''))
            sender_street = st.text_input("Sender Street", value=selected_profile.get('street', ''))
            sender_zip = st.text_input("Sender ZIP Code", value=selected_profile.get('zip_code', ''))
            sender_city = st.text_input("Sender City", value=selected_profile.get('city', ''))
        with col2:
            sender_phone = st.text_input("Sender Phone", value=selected_profile.get('phone', ''))
            sender_email = st.text_input("Sender Email", value=selected_profile.get('email', ''))
            
        st.subheader("Recipient Information")
        recipient_company = render_locked_input("Company / Authority", "recipient_company")
        recipient_department = render_locked_input("Department / PO Box (Optional)", "recipient_department")
        recipient_street = render_locked_input("Recipient Street (leave empty if PO Box)", "recipient_street")
        recipient_zip = render_locked_input("Recipient ZIP Code", "recipient_zip")
        recipient_city = render_locked_input("Recipient City", "recipient_city")
            
        st.subheader("Date & Subject")
        ort = render_locked_input("Location", "ort", default_val=selected_profile.get('city', ''))
        datum = render_locked_input("Date", "datum", default_val=datetime.datetime.now().strftime("%d.%m.%Y"))
        job_title = render_locked_input("Subject", "job_title", default_val="Bewerbung als ... (Kennziffer ...)")
            
        st.subheader("Letter Contents")
        salutation = render_locked_input("Salutation", "salutation", default_val="Sehr geehrte Damen und Herren,", max_chars=100)
        einleitung = render_locked_input("Introduction (Paragraph 1)", "einleitung", is_textarea=True, max_chars=400, placeholder="Max 400 characters to keep it on one page...")
        absatz1 = render_locked_input("Main Body Paragraph 1", "absatz1", is_textarea=True, max_chars=800, placeholder="Max 800 characters to keep it on one page...")
        absatz2 = render_locked_input("Main Body Paragraph 2", "absatz2", is_textarea=True, max_chars=800, placeholder="Max 800 characters to keep it on one page...")
        absatz3 = render_locked_input("Main Body Paragraph 3 (optional)", "absatz3", is_textarea=True, max_chars=600, placeholder="Max 600 characters to keep it on one page...")
        schlusssatz = render_locked_input("Closing Sentence", "schlusssatz", default_val="Ich freue mich auf Ihre Einladung.", max_chars=200, placeholder="Max 200 characters...")
        grussformel = render_locked_input("Valediction", "grussformel", default_val="Mit freundlichen Grüßen,", max_chars=100)
        
        if st.button("Generate Document"):
            template_path = os.path.join('cover', 'din5008_bewerbung_vorlage.docx')
            if not os.path.exists(template_path):
                st.error(f"Template '{template_path}' not found.")
            else:
                try:
                    daten = {
                        "ABSENDER_NAME": sender_name,
                        "ABSENDER_STRASSE": sender_street,
                        "ABSENDER_PLZ": sender_zip,
                        "ABSENDER_ORT": sender_city,
                        "ABSENDER_TELEFON": sender_phone,
                        "ABSENDER_EMAIL": sender_email,
                        "EMPFAENGER_FIRMA": recipient_company,
                        "EMPFAENGER_ABTEILUNG": recipient_department,
                        "EMPFAENGER_STRASSE": recipient_street,
                        "EMPFAENGER_PLZ": recipient_zip,
                        "EMPFAENGER_ORT": recipient_city,
                        "ORT": ort,
                        "DATUM": datum,
                        "BETREFF": job_title + "\n",
                        "ANREDE": salutation,
                        "EINLEITUNGSSATZ": einleitung,
                        "HAUPTTEIL_ABSATZ_1": absatz1,
                        "HAUPTTEIL_ABSATZ_2": absatz2,
                        "HAUPTTEIL_ABSATZ_3": absatz3,
                        "SCHLUSSSATZ": schlusssatz,
                        "GRUSSFORMEL": grussformel,
                        "ABSENDER_VOLLNAME": sender_name,
                    }
                    
                    docx_bytes = vorlage_befuellen(template_path, daten, selected_font)
                    
                    st.success("Document generated successfully!")
                    st.download_button(
                        label="Download Cover Letter (.docx)",
                        data=docx_bytes,
                        file_name=f"Cover_Letter_{sender_name.replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.error(f"Error generating document: {e}")
