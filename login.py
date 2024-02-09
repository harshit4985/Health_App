import sqlite3

import anvil
import requests
from anvil.tables import app_tables
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

class Login(MDScreen):
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
    def is_connected(self):
        try:
            # Attempt to make a simple HTTP request to check connectivity
            response = requests.get('https://www.google.com', timeout=1)
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
            self.manager.load_screen("menu_profile")
            self.manager.push_replacement("client_services")
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
            screen = self.manager.get_screen('menu_profile')
            screen.ids.username.text = f"Username : {username}"
            screen.ids.email.text = f"Email : {email}"
            screen.ids.phone.text = f"Phone no : {phone}"
            screen.ids.pincode.text = f"Pincode : {pincode}"
            screen1 = self.manager.get_screen('client_services')
            screen1.ids.username.text = username
            screen1.ids.email.text = email

        else:
            # Login failed
            self.ids.login_email.error = True
            self.ids.login_email.helper_text = "Invalid email or password"
            self.ids.login_password.error = True
