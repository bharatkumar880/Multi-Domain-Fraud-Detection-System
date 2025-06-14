import streamlit as st
import sqlite3
import base64
import requests
import random
import time


class UserAuthApp:
    def __init__(self):
        self.init_db()
        self.set_background_image("C:/Users/HP/Downloads/FraudFortify/FraudFortify/Images/back2.jpg")  # Replace with your main background image path
        self.set_sidebar_background("C:/Users/HP/Downloads/FraudFortify/FraudFortify/Images/side.png") # Replace with your sidebar background image path
        self.TELEGRAM_TOKEN = "7501242677:AAEr_IF4AlsU1xqWI041UQyNDfB2sGrEp7c"
        self.TELEGRAM_CHAT_ID = "903868226"

        # Initialize OTP session state variables
        if "random_number" not in st.session_state:
            st.session_state.random_number = None
        if "start_time" not in st.session_state:
            st.session_state.start_time = None
        if "timer_running" not in st.session_state:
            st.session_state.timer_running = False
        if "is_code_expired" not in st.session_state:
            st.session_state.is_code_expired = False

    def get_base64_of_bin_file(self, bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def set_background_image(self, image_path):
        background_image = self.get_base64_of_bin_file(image_path)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{background_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    def set_sidebar_background(self, sidebar_image_path):
        sidebar_background_image = self.get_base64_of_bin_file(sidebar_image_path)
        st.markdown(
            f"""
            <style>
            [data-testid="stSidebar"] {{
                background-image: url("data:image/jpg;base64,{sidebar_background_image}");
                background-size: cover;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    def init_db(self):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT UNIQUE,
                name TEXT,
                last_name TEXT,
                email TEXT UNIQUE,
                location TEXT
            )
        """)
        conn.commit()
        conn.close()

    def register_user(self, username, name, last_name, email, location):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("""
                INSERT INTO users (username, name, last_name, email, location)
                VALUES (?, ?, ?, ?, ?)
            """, (username, name, last_name, email, location))
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.close()
            if "UNIQUE constraint failed" in str(e):
                if "username" in str(e):
                    return "Username already exists."
                elif "email" in str(e):
                    return "Email already registered."
            return "Registration failed."
        conn.close()
        return "Success"

    def authenticate_user(self, username):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        return user is not None

    def send_otp_to_telegram(self):
        """Generate a random number and send it to Telegram."""
        st.session_state.random_number = random.randint(1000, 9999)
        st.session_state.start_time = time.time()
        st.session_state.timer_running = True
        st.session_state.is_code_expired = False
        message = f"Your authentication code is: {st.session_state.random_number}"
        url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": self.TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            st.success("Authentication code sent to your Telegram!")
        else:
            st.error("Failed to send authentication code to Telegram.")

    def authenticate_with_otp(self, entered_number):
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

    def login_ui(self):
        st.subheader("Login with OTP")
        username = st.text_input("Username")
        if st.button("Send OTP"):
            if self.authenticate_user(username):
                self.send_otp_to_telegram()
            else:
                st.error("Invalid username")

        # Timer display and OTP input
        if st.session_state.timer_running:
            elapsed_time = time.time() - st.session_state.start_time
            remaining_time = max(0, 30 - elapsed_time)
            st.write(f"Time remaining to enter the code: **{int(remaining_time)} seconds**")
            if remaining_time == 0:
                st.session_state.timer_running = False
                st.session_state.is_code_expired = True
        entered_code = st.text_input("Enter the OTP sent to Telegram:", type="password")
        if st.button("Authenticate"):
            if entered_code.isdigit():
                if self.authenticate_with_otp(int(entered_code)):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success(f"Welcome {username}!")
            else:
                st.error("Invalid OTP")

    def register_ui(self):
        st.subheader("Create New Account")
        name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        location = st.text_input("Location")
        new_username = st.text_input("Username")

        if st.button("Register"):
            registration_result = self.register_user(new_username, name, last_name, email, location)
            if registration_result == "Success":
                st.success("Account created successfully! You can now log in with OTP.")
            else:
                st.error(registration_result)

    def logout(self):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.info("You have been logged out.")

    def main(self):
        # Check if the user is already logged in
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
            st.session_state['username'] = None

        st.title("User Authentication")
        menu = ["Register", "OTP Login"]
        choice = st.selectbox("Select an Option", menu)

        if choice == "Register":
            self.register_ui()
        elif choice == "OTP Login":
            self.login_ui()


if __name__ == '__main__':
    app = UserAuthApp()
    app.main()
