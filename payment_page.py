import razorpay
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

Builder.load_file("payment_page.kv")

class Payment(MDScreen):
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

        except Exception as e:
            print("An error occurred while creating the order:", str(e))

    def open_payment_gateway(self, payment_url):
        # Replace this with actual code to open the payment gateway URL
        print(f"Opening Razorpay payment gateway: {payment_url}")
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
