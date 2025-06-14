import streamlit as st
import requests
import random
import time
import datetime

# Telegram bot details
TELEGRAM_TOKEN = "7047754135:AAG8fFEA1lDVe21bQYYTozv3gb_wpf3-5hs"
TELEGRAM_CHAT_ID = "1893904443"

# Initialize session state variables
if "random_number" not in st.session_state:
    st.session_state.random_number = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "is_code_expired" not in st.session_state:
    st.session_state.is_code_expired = False


def send_random_number_to_telegram():
    """Generate a random number and send it to Telegram."""
    st.session_state.random_number = random.randint(1000, 9999)
    st.session_state.start_time = time.time()
    st.session_state.timer_running = True
    st.session_state.is_code_expired = False
    message = f"Your authentication code is: {st.session_state.random_number}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        st.success("Authentication code sent to your Telegram!")
    else:
        st.error("Failed to send authentication code to Telegram.")


def authenticate_user(entered_number):
    """Check if the entered number is correct and within the 30-second window."""
    if st.session_state.is_code_expired:
        st.error("The authentication code has expired. Please generate a new code.")
        return False
    if not st.session_state.random_number or not st.session_state.start_time:
        st.error("Please generate and send the code first!")
        return False
    elapsed_time = time.time() - st.session_state.start_time
    if elapsed_time > 30:
        st.error("Time expired! Please request a new authentication code.")
        st.session_state.is_code_expired = True
        st.session_state.timer_running = False
        return False
    if entered_number == st.session_state.random_number:
        st.success("Authentication successful! Welcome!")
        st.session_state.timer_running = False
        return True
    else:
        st.error("Invalid authentication code.")
        return False


# Streamlit UI
st.title("Secure Login System")
st.write("Authenticate yourself using a Telegram code.")

# Button to send the code to Telegram
if st.button("Send Authentication Code to Telegram"):
    send_random_number_to_telegram()

# Timer display
if st.session_state.timer_running:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, 30 - elapsed_time)
    formatted_time = str(datetime.timedelta(seconds=int(remaining_time)))
    st.write(f"Time remaining to enter the code: **{formatted_time}**")
    if remaining_time == 0:
        st.session_state.timer_running = False
        st.session_state.is_code_expired = True

# Input field for the user to enter the received code
entered_code = st.text_input("Enter the code you received on Telegram:", value="", type="password")

# Button to authenticate the user
if st.button("Authenticate"):
    if entered_code.isdigit():
        authenticate_user(int(entered_code))
    else:
        st.error("Please enter a valid numeric code.")
