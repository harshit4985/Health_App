import sqlite3
import webbrowser

import razorpay
from anvil.tables import app_tables
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivymd.app import MDApp
import anvil


class Payment(MDScreen):
    # def payment_page_backButton(self):
    #     # Extract the username from menu_profile
    #     self.screen = Builder.load_file("menu_profile.kv")
    #     screen = self.root.get_screen('menu_profile')
    #     username = screen.ids.username.text
    #     print(username)
    #     conn = sqlite3.connect("users.db")
    #     cursor = conn.cursor()
    #     # Execute the SQL DELETE statement
    #     cursor.execute("DELETE FROM BookSlot WHERE username = ?", (username,))
    #     # Commit the changes and close the connection
    #     conn.commit()
    #     self.root.transition.direction='right'
    #     self.root.current = 'slot_booking'
    def razor_pay(self, instance):
        client = razorpay.Client(auth=('rzp_test_kOpS7Ythlfb1Ho', 'OzPZyPbsOV0AlADilk4wkgv9'))

        # Create an order
        order_amount = 5000  # Amount in paise (e.g., 50000 paise = 500 INR)
        order_currency = 'INR'
        order_receipt = 'order_rcptid_12'

        order_data = {
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'payment_capture': 1  # Automatically capture payment when order is created
        }
        try:
            order = client.order.create(data=order_data)
            # Get the order ID
            order_id = order['id']
            # client.payment.launch(order_id)

            # Construct the payment URL
            payment_url = f"https://rzp_test_kOpS7Ythlfb1Ho.api.razorpay.com/v1/checkout/{order_id}"
            self.open_payment_gateway(payment_url)
            self.show_validation_dialog("Payment Successful")
            anvil.server.connect("server_UY47LMUKBDUJMU4EA3RKLXCC-LP5NLIEYMCLMZ4NU")
            screen = self.manager.get_screen('client_services')
            email = screen.ids.email.text
            user_name = self.ids.user_name.text
            book_date = self.ids.session_date.text
            book_time = self.ids.session_time.text
            user = app_tables.users.get(email=email)
            user_id = user['id']
            row = app_tables.book_slot.search()
            slot_id = len(row) + 1
            app_tables.book_slot.add_row(
                slot_id=slot_id,
                user_id=user_id,
                username=user_name,
                book_date=book_date,
                book_time=book_time
            )
        except Exception as e:
            print("An error occurred while creating the order:", str(e))

    def open_payment_gateway(self):
        # Replace this with actual code to open the payment gateway URL
        print(f"Opening Razorpay payment gateway")
        website_url = 'https://rzp.io/l/iJyrLCI'
        webbrowser.open(website_url)
        # # Create the Razorpay checkout URL
        # razorpay_key_id = 'rzp_test_kOpS7Ythlfb1Ho'
        # razorpay_checkout_url = f'https://checkout.razorpay.com/v1/checkout.js?key={razorpay_key_id}'
        # webbrowser(razorpay_checkout_url)

        # Open the Razorpay checkout in a WebView
        # webbrowser.create_window('Razorpay Checkout', razorpay_checkout_url, width=800, height=600, resizable=True)
        #
        # # payment_page page logic
        # layout = BoxLayout(orientation='vertical')
        #
        # # Create a WebView to display the Razorpay payment page
        # webview = WebView(url='payment_url', size_hint=(1, 1))
        # layout.add_widget(webview)
        #
        # # Add a back button
        # back_button = Button(text='Back to App', size_hint=(1, 0.1))
        # back_button.bind(on_press=self.back_to_app)
        # layout.add_widget(back_button)
        #
    # def open_payment_gateway(self, payment_url):
    #     # Replace this with actual code to open the payment gateway URL
    #     print(f"Opening Razorpay payment gateway: {payment_url}")
    #
    #     # payment_page page logic
    #     layout = BoxLayout(orientation='vertical')
    #
    #     # Create a WebView to display the Razorpay payment page
    #     webview = WebView(url='payment_url', size_hint=(1, 1))
    #     layout.add_widget(webview)
    #
    #     # Add a back button
    #     back_button = Button(text='Back to App', size_hint=(1, 0.1))
    #     back_button.bind(on_press=self.back_to_app)
    #     layout.add_widget(back_button)

        # return layout

    # def on_pay_button_pressed(self, instance):
    #     client = razorpay.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")
    #
    #     order = client.order.create(amount=10000, currency="INR")
    #
    #     client.payment.launch(order_id=order["id"])
    #
    #     client.payment.on("success", self.on_payment_success)
    #
    # def on_payment_success(self, payment):
    #     self.label.text = "Payment successful!"

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
