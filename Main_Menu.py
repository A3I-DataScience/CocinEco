__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os
import re  # For regex validation
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(
    page_title="CocinEco",
    page_icon="cocineco_browser_icon.png",
)


# Function to validate email format
def is_valid_email(email):
    """Returns True if email is valid, False otherwise."""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email)


def send_email(name, email, message):
    sender_email = "antoine.a3isp@gmail.com"  # Replace with your Gmail address
    receiver_email = (
        "cocineco-contact@math-clais.ovh"  # Replace with the email that receives messages
    )

    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    # Create an email message with UTF-8 encoding
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Attach the message body with UTF-8 encoding
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, st.secrets["GMAIL_APP_PWD"])
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        return str(e)


def contact_form():

    # Set page title
    st.subheader("📩 Contact Us")

    # Create form for user input
    with st.form(key="contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")

        # Submit button inside the form
        submit_button = st.form_submit_button(label="Send Message")

    # Handling form submission
    if submit_button:
        if not name or not email or not message:
            st.error("⚠️ Please fill in all fields before submitting.")
        elif not is_valid_email(email):
            st.error("❌ Invalid email format. Please enter a valid email address.")
        else:

            status_to_you = send_email(name, email, message)

            subject_to_sender = "✅ Thank You for Contacting Us"
            body_to_sender = (
                f"Hello {name},\n\n"
                + "Thank you for reaching out! We've received your message and will get back to you soon.\n\n"
                + "Your Message:\n"
                + f"{message}\n\n"
                + "Best regards,\nYour Business Name"
            )
            status_to_sender = send_email(email, subject_to_sender, body_to_sender)

            # Show success or error messages
            if status_to_you is True and status_to_sender is True:
                st.success(
                    f"✅ Thank you {name}, your message has been sent. A confirmation email has also been sent to {email}."
                )
            else:
                st.error(
                    f"⚠️ Error sending message: {status_to_you if status_to_you is not True else status_to_sender}"
                )


def is_running_on_streamlit_cloud():
    # Check if "is_cloud" exists in secrets and is set to true
    #running_on_cloud = st.secrets.get("general", {}).get("is_cloud", False)
    running_on_cloud = os.getenv("is_cloud")

    if running_on_cloud:
        pass
    else:
        st.warning("running on local")
    return running_on_cloud


def init_cocineco():
    if is_running_on_streamlit_cloud():
        st.session_state.use_authentication = True
        st.session_state.running_in_cloud = True
    else:
        st.session_state.use_authentication = False
        st.session_state.running_in_cloud = False

    if "authenticated_user" not in st.session_state:
        st.session_state.authenticated_user = False


def authenticate_user():
    correct_username = "cocineco-admin"
    correct_password = "cocineco-admin-2025"

    # Prompt the user for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    st.session_state.authenticated_user = (
        username == correct_username
    )  # and password == correct_password)
    st.markdown("Please enter your Username and Password.")

    if st.button("Login"):
        if st.session_state.authenticated_user:
            st.success("Login successful!")
        else:
            st.error(
                "Please login to access CocinEcoBot. To obtain a Username and Password please use the form below."
            )


def main():

    st.image("cocineco_banner_with_logo.png")

    st.markdown(
        "Please, help us understanding your needs and interests answering our [survey](https://docs.google.com/forms/d/e/1FAIpQLSduSvvWUvwmEeH1ckVlPGgcIL8sTDTDqRMx7LwUkYYiNH-SHg/viewform?usp=sharing)."
    )

    init_cocineco()

    if not st.session_state.authenticated_user and st.session_state.use_authentication:

        authenticate_user()

    else:
        st.session_state.authenticated_user = True
        st.sidebar.success("Select a Planner Above.")

    contact_form()


main()
