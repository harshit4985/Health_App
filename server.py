import socket
import sqlite3
import anvil
import requests


class Server:

    def is_connected(self):
        try:
            # Attempt to create a socket connection to google.com
            print("Internet is connected")
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False

    def get_database_connection(self):
        if self.is_connected():  # Use the stored connection status
            # Use Anvil's database connection
            print("Connected to anvil.server")
            return anvil.server.connect("server_UY47LMUKBDUJMU4EA3RKLXCC-LP5NLIEYMCLMZ4NU")
        else:
            # Use SQLite database connection
            print("Connected to sqlite3")
            return sqlite3.connect('users.db')

    def sqlite3_users_db(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                phone TEXT NOT NULL,
                pincode TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Connected to sqlite3")
        return sqlite3.connect('users.db')
