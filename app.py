import streamlit as st
import datetime
import io
import os
from docxtpl import DocxTemplate
from database import init_db, create_user, verify_user, save_profile, get_all_profiles, delete_profile

# Initialize DB on start
init_db()

st.set_page_config(page_title="applyfly", page_icon="📄", layout="wide")

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
            new_city_zip = st.text_input("City and ZIP Code")
            new_phone = st.text_input("Phone Number")
            new_email = st.text_input("Email Address")
            
            if st.button("Save Profile"):
                if new_profile_name and new_name and new_street and new_city_zip and new_phone and new_email:
                    save_profile(st.session_state.user_email, new_profile_name, new_name, new_street, new_phone, new_email, new_city_zip)
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
        
        profiles = get_all_profiles(st.session_state.user_email)
        profile_options = {p['profile_name']: p for p in profiles}
        
        selected_profile_name = st.selectbox("Select Sender Profile", options=["-- Select a Profile --"] + list(profile_options.keys()))
        
        selected_profile = profile_options.get(selected_profile_name, {}) if selected_profile_name != "-- Select a Profile --" else {}
        
        st.subheader("Sender Information")
        col1, col2 = st.columns(2)
        with col1:
            sender_name = st.text_input("Sender Name", value=selected_profile.get('name', ''))
            sender_street = st.text_input("Sender Street", value=selected_profile.get('street', ''))
            sender_city_zip = st.text_input("Sender City & ZIP", value=selected_profile.get('city_zip', ''))
        with col2:
            sender_phone = st.text_input("Sender Phone", value=selected_profile.get('phone', ''))
            sender_email = st.text_input("Sender Email", value=selected_profile.get('email', ''))
            
        st.subheader("Recipient Information")
        col3, col4 = st.columns(2)
        with col3:
            recipient_company = st.text_input("Company Name")
            recipient_department = st.text_input("Department (Optional)")
        with col4:
            recipient_street = st.text_input("Recipient Street")
            recipient_city_zip = st.text_input("Recipient City & ZIP")
            
        st.subheader("Letter Details")
        job_title = st.text_input("Job Title / Application Subject")
        salutation = st.text_input("Salutation (e.g., Sehr geehrte Damen und Herren,)")
        
        cover_letter_body = st.text_area("Cover Letter Body", height=250)
        
        if st.button("Generate Document"):
            if not os.path.exists('din_5008_template.docx'):
                st.error("Template 'din_5008_template.docx' not found. Please create it according to the README.")
            else:
                try:
                    # Current date
                    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
                    
                    # Extract city from sender_city_zip (e.g., "12345 Berlin" -> "Berlin")
                    city = ""
                    if sender_city_zip:
                        parts = sender_city_zip.strip().split(maxsplit=1)
                        if len(parts) > 1 and parts[0].isdigit():
                            city = parts[1]
                        else:
                            city = sender_city_zip.strip()
                            
                    date_context = f"{city}, den {current_date}" if city else current_date
                    
                    context = {
                        'sender_name': sender_name,
                        'sender_street': sender_street,
                        'sender_city_zip': sender_city_zip,
                        'sender_phone': sender_phone,
                        'sender_email': sender_email,
                        'recipient_company': recipient_company,
                        'recipient_department': recipient_department,
                        'recipient_street': recipient_street,
                        'recipient_city_zip': recipient_city_zip,
                        'job_title': job_title,
                        'salutation': salutation,
                        'date': date_context,
                        'cover_letter_body': cover_letter_body
                    }
                    
                    doc = DocxTemplate('din_5008_template.docx')
                    doc.render(context)
                    
                    # Save to BytesIO
                    bio = io.BytesIO()
                    doc.save(bio)
                    
                    st.success("Document generated successfully!")
                    st.download_button(
                        label="Download Cover Letter (.docx)",
                        data=bio.getvalue(),
                        file_name=f"Cover_Letter_{sender_name.replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.error(f"Error generating document: {e}")
