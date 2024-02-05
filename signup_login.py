import sqlite3
import re
import anvil
import requests
from anvil import Timer
from anvil.tables import app_tables
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from twilio.rest import Client

Builder.load_file("signup.kv")
Builder.load_file("login.kv")
Builder.load_file("forgot_password.kv")

class Connection:
    def is_connected(self):
        try:
            # Attempt to make a simple HTTP request to check connectivity
            response = requests.get('https://www.google.com', timeout=5)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return True
        except requests.RequestException:
            return False

    def get_database_connection(self):
        if self.is_connected():
            # Use Anvil's database connection
            return anvil.server.connect("server_UY47LMUKBDUJMU4EA3RKLXCC-LP5NLIEYMCLMZ4NU")
        else:
            # Use SQLite database connection
            return sqlite3.connect('users.db')

    def show_validation_dialog(self, message):
        # Create the dialog asynchronously
        Clock.schedule_once(lambda dt: self._create_dialog(message), 0)

    def _create_dialog(self, message):
        dialog = MDDialog(
            text=f"{message}",
            elevation=0,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

    # def google_sign_in(self):
    #     # Set up the OAuth 2.0 client ID and client secret obtained from the Google Cloud Console
    #     client_id = "749362207551-tdoq2d8787csqqnbvpdgcc3m2sdtsnd1.apps.googleusercontent.com"
    #     client_secret = "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"
    #     redirect_uri = "https://oxivive.com/oauth/callback"
    #     redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    #
    #     # Set up the Google OAuth flow
    #     flow = InstalledAppFlow.from_client_secrets_file(
    #         "client_secret.json",
    #         scopes=["https://www.googleapis.com/auth/userinfo.email"],
    #         redirect_uri=redirect_uri
    #     )
    #
    #     # Get the authorization URL
    #     auth_url, _ = flow.authorization_url(prompt="select_account")
    #     print(f"Authorization URL: {auth_url}")
    #
    #     # Open a web browser to the authorization URL
    #     webbrowser.open(auth_url)
    #
    #     # Get the authorization code from the user
    #     authorization_code = input("Enter the authorization code: ")
    #
    #     # Exchange the authorization code for credentials
    #     credentials = flow.fetch_token(
    #         token_uri="https://oauth2.googleapis.com/token",
    #         authorization_response=authorization_code
    #     )
    #
    #     # Use the obtained credentials for further Google API requests
    #     # Example: print the user's email address
    #     user_email = credentials.id_token["email"]
    #     print(f"User email: {user_email}")
    #
    # def exchange_code_for_tokens(self, authorization_code):
    #     token_url = "https://oauth2.googleapis.com/token"
    #
    #     params = {
    #         "code": authorization_code,
    #         "client_id": "your_client_id",
    #         "client_secret": "your_client_secret",
    #         "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    #         "grant_type": "authorization_code"
    #     }
    #
    #     response = requests.post(token_url, data=params)
    #     token_data = response.json()
    #
    #     return token_data


class Signup(MDScreen, Connection):
    def users(self, instance, *args):

        username = self.ids.signup_username.text
        email = self.ids.signup_email.text
        password = self.ids.signup_password.text
        phone = self.ids.signup_phone.text
        pincode = self.ids.signup_pincode.text

        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        # Enhanced password validation
        is_valid_password, password_error_message = self.validate_password(password)
        # Clear existing helper texts
        self.ids.signup_username.helper_text = ""
        self.ids.signup_email.helper_text = ""
        self.ids.signup_password.helper_text = ""
        self.ids.signup_phone.helper_text = ""
        self.ids.signup_pincode.helper_text = ""
        if not username:
            self.ids.signup_username.error = True
            self.ids.signup_username.helper_text = "Enter Name"
        elif not email or not re.match(email_regex, email):
            self.ids.signup_email.error = True
            self.ids.signup_email.helper_text = "Invalid Email"
        elif not is_valid_password:
            self.ids.signup_password.error = True
            self.ids.signup_password.helper_text = password_error_message
        elif not phone or len(phone) != 10:
            self.ids.signup_phone.error = True
            self.ids.signup_phone.helper_text = "Invalid Phone number (10 digits required)"
        elif not pincode or len(pincode) != 6:
            self.ids.signup_pincode.error = True
            self.ids.signup_pincode.helper_text = "Invalid Pincode (6 digits required)"

        else:
            # Clear any existing errors and helper texts
            self.ids.signup_username.error = False
            self.ids.signup_username.helper_text = ""
            self.ids.signup_email.error = False
            self.ids.signup_email.helper_text = ""
            self.ids.signup_password.error = False
            self.ids.signup_password.helper_text = ""
            self.ids.signup_phone.error = False
            self.ids.signup_phone.helper_text = ""
            self.ids.signup_pincode.error = False
            self.ids.signup_pincode.helper_text = ""

            # clear input texts
            self.ids.signup_username.text = ""
            self.ids.signup_email.text = ""
            self.ids.signup_password.text = ""
            self.ids.signup_phone.text = ""
            self.ids.signup_pincode.text = ""

            # If validation is successful, insert into the database
            try:
                if self.is_connected():
                    anvil.server.connect("server_UY47LMUKBDUJMU4EA3RKLXCC-LP5NLIEYMCLMZ4NU")
                    rows = app_tables.users.search()
                    # Get the number of rows
                    id = len(rows) + 1
                    app_tables.users.add_row(
                        id=id,
                        username=username,
                        email=email,
                        password=password,
                        phone=float(phone),
                        pincode=int(pincode))
                    connection = sqlite3.connect('users.db')
                    cursor = connection.cursor()
                    cursor.execute('''
                                    INSERT INTO users (username, email, password, phone, pincode)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (username, email, password, phone, pincode))
                    connection.commit()
                    connection.close()
                else:
                    self.show_validation_dialog("No internet connection")

            except Exception as e:
                print(e)
                self.show_validation_dialog("No internet connection")
            # Navigate to the success screen
            app = MDApp.get_running_app()
            app.root.transition.direction = "left"
            app.root.current = "login"

    # password validation
    def validate_password(self, password):
        # Check if the password is not empty
        if not password:
            return False, "Password cannot be empty"
        # Check if the password has at least 8 characters
        if len(password) < 6:
            return False, "Password must have at least 6 characters"
        # Check if the password contains both uppercase and lowercase letters
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return False, "Password must contain uppercase, lowercase"
        # Check if the password contains at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        # Check if the password contains at least one special character
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_characters, password):
            return False, "Password must contain a special character"
        # All checks passed; the password is valid
        return True, "Password is valid"

    # def show_validation_dialog(self, message):
    #     # Display a dialog for invalid login or sign up
    #     dialog = MDDialog(
    #         text=message,
    #         elevation=0,
    #         buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
    #     )
    #     dialog.open()


class Login(MDScreen, Connection):

    def login_page(self, instance, *args):
        email = self.ids.login_email.text
        password = self.ids.login_password.text

        connection = self.get_database_connection()
        user_anvil = None
        user_sqlite = None
        try:
            if self.is_connected():
                # Fetch user from Anvil's database
                user_anvil = app_tables.users.get(
                    email=email,
                    password=password,
                )
            else:
                # Fetch user from SQLite database
                cursor = connection.cursor()
                cursor.execute('''
                            SELECT * FROM users
                            WHERE email = ? AND password = ?
                        ''', (email, password))
                user_sqlite = cursor.fetchone()
        finally:
            # Close the connection
            if connection and self.is_connected():
                connection.close()
        if user_anvil or user_sqlite:
            print("Login successful.")
            app = MDApp.get_running_app()
            app.root.transition.direction = "left"
            app.root.current = "client_services"
            if user_anvil:
                username = str(user_anvil["username"])
                email = str(user_anvil["email"])
                phone = str(user_anvil["phone"])
                pincode = str(user_anvil["pincode"])
            elif user_sqlite:
                username = str(user_sqlite[1])
                email = str(user_sqlite[2])
                phone = str(user_sqlite[4])
                pincode = str(user_sqlite[5])
            screen = app.root.get_screen('menu_profile')
            screen.ids.username.text = f"Username : {username}"
            screen.ids.email.text = f"Email : {email}"
            screen.ids.phone.text = f"Phone no : {phone}"
            screen.ids.pincode.text = f"Pincode : {pincode}"
            screen3 = app.root.get_screen('client_services')
            screen3.ids.username.text = username
            screen3.ids.email.text = email

        else:
            # Login failed
            self.ids.login_email.error = True
            self.ids.login_email.helper_text = "Invalid email or password"
            self.ids.login_password.error = True


# Your Twilio credentials
account_sid = "AC64ab0fed3c9135f8011fb5e50f969cbe"
auth_token = "6749dd3de2d4165a71ee9fec341ae503"
verify_sid = "VA8937ab1f8c09c4e3842e4b32f72c8dc7"
verified_number = "+919108340960"

# Initialize Twilio client
client = Client(account_sid, auth_token)


class Forgot_password(MDScreen):

    def show_validation_dialog(self, message):
        # Create the dialog asynchronously
        Clock.schedule_once(lambda dt: self._create_dialog(message), 0)

    def _create_dialog(self, message):
        dialog = MDDialog(
            text=f"{message}",
            elevation=0,
        )
        dialog.open()
    def validate_password(self, password):
        # Check if the password is not empty
        if not password:
            return False, "Password cannot be empty"
        # Check if the password has at least 8 characters
        if len(password) < 6:
            return False, "Password must have at least 6 characters"
        # Check if the password contains both uppercase and lowercase letters
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return False, "Password must contain uppercase, lowercase"
        # Check if the password contains at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        # Check if the password contains at least one special character
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_characters, password):
            return False, "Password must contain a special character"
        # All checks passed; the password is valid
        return True, "Password is valid"

    def change_password(self):
        phone = float(self.ids.phone.text)
        new_password = self.ids.new_password.text
        is_valid_password, password_error_message = self.validate_password(new_password)
        self.ids.change_password.disabled = False
        anvil.server.connect("server_UY47LMUKBDUJMU4EA3RKLXCC-LP5NLIEYMCLMZ4NU")
        record = app_tables.users.get(phone=phone)
        if not is_valid_password:
            self.ids.new_password.error = True
            self.ids.new_password.helper_text = password_error_message

        else:
            if record:
                record.update(password=new_password)
                print("changed")

    def sent_otp(self):
        phone = self.ids.phone.text

        if not (phone and len(phone) == 10):
            self.handle_invalid_phone()
        else:
            phone_number = f"+91{phone}"
            try:
                # Send OTP via Twilio
                verification = client.verify.v2.services(verify_sid).verifications.create(
                    to=phone_number, channel="sms"
                )
                self.update_ui_on_otp_sent(phone_number)
            except Exception as e:
                self.handle_otp_sending_error(e)

    def handle_invalid_phone(self):
        self.ids.phone.error = True
        self.ids.phone.helper_text = "Invalid Phone number (10 digits required)"

    def update_ui_on_otp_sent(self, phone_number):
        print(f"OTP sent to {phone_number}")
        self.ids.sent_otp.text = "Sent"
        self.ids.sent_otp.color = (0, 1, 0, 1)
        self.ids.otp.disabled = False
        self.ids.verify_otp.disabled = False

    def handle_otp_sending_error(self, e):
        self.show_validation_dialog("No internet connection")

    def verify_otp(self):
        phone_number = f"+91{self.ids.phone.text}"
        user_entered_otp = self.ids.otp.text
        try:
            # Verify OTP via Twilio
            verification_check = client.verify.v2.services(verify_sid) \
                .verification_checks \
                .create(to=phone_number, code=user_entered_otp)
            if verification_check.status == 'approved':
                self.update_ui_on_otp_verified()
            else:
                self.handle_invalid_otp()
        except Exception as e:
            self.handle_otp_verification_error(e)

    def update_ui_on_otp_verified(self):
        print("OTP verified")
        self.ids.verify_otp.text = "Verified"
        self.ids.verify_otp.color = (0, 1, 0, 1)
        self.ids.new_password.disabled = False
        self.change_password()

    def handle_invalid_otp(self):
        self.show_validation_dialog("Invalid OTP")

    def handle_otp_verification_error(self, e):
        self.show_validation_dialog("Error Occurred")


