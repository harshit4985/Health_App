import re
import sqlite3

# from android.permissions import request_permissions, Permission
from anvil import BlobMedia
from anvil.tables import app_tables
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivy.properties import ObjectProperty
from kivymd.uix.filemanager import MDFileManager
from kivymd.app import MDApp
import anvil.server
import anvil.media
import os
import requests
from kivymd.uix.scrollview import MDScrollView

Builder.load_file('service_register.kv')
kv = Builder.load_file('content_class.kv')
conn = sqlite3.connect("user.db")
cursor = conn.cursor()

# Creating the hospital_table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS hospital_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_name TEXT,
        established_year TEXT,
        District TEXT,
        State TEXT,
        pincode TEXT,
        address TEXT,
        doc1 BLOB,
        doc2 BLOB
    )
''')

# Creating the mobile_hospital_table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mobile_hospital_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT,
        model_year TEXT,
        District TEXT,
        State TEXT,
        pincode TEXT,
        address TEXT,
        doc1 BLOB,
        doc2 BLOB
    )
''')

# Creating the oxi_gym_table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS oxi_gym_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        oxi_gym_name TEXT,
        established_year TEXT,
        District TEXT,
        State TEXT,
        pincode TEXT,
        address TEXT,
        doc1 BLOB,
        doc2 BLOB
    )
''')

conn.commit()
conn.close()


class BaseRegistrationScreen(MDScreen):
    def request_permissions(self):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    def show_date_picker(self, arg):
        date_dialog = MDDatePicker(size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
        self.ids.extra_info2.text = ''

    def on_save(self, instance, value, date_range):
        self.ids.extra_info2.text = str(value)

    # click Cancel
    def on_cancel(self, instance, value):
        # print("cancel")
        instance.dismiss()

    # ------------------------------upload--docs--------------------------
    field_id = None

    def file_manager_open(self, field_id):
        self.field_id = getattr(self.ids, field_id)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            # use_saf=True,

        )
        self.file_manager.show('/')  # Initial directory when the file manager is opened

    path = None

    def select_path(self, path):
        if path.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf')):
            self.path = path
            setattr(self.field_id, 'text', path)
            self.file_manager.close()
        else:
            msg = "Please select a JPG, PNG, or PDF file."
            setattr(self.field_id, 'text', msg)
        self.file_manager.close()

    file_data1 = None
    file_data2 = None
    file_name1 = None
    file_name2 = None

    def upload_file(self, upload_id):
        try:
            file_path = getattr(self.field_id, 'text', '')
            if file_path:
                file_name = os.path.basename(file_path)
                file_data = self.read_file(file_path)
                setattr(self.field_id, 'text', file_name)

                if upload_id == "file_path":
                    self.file_data1 = file_data
                    self.file_name1 = file_name
                    self.field_id = None
                    print(self.file_data1)
                elif upload_id == "file_path2":
                    self.file_data2 = file_data
                    self.file_name2 = file_name
                    self.field_id = None
                    print(self.file_data2)
        except:
            msg = "Please select a file."
            setattr(self.field_id, 'text', msg)

    def read_file(self, file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    def exit_manager(self, *args):
        self.file_manager.close()

    # ----------------------------------registration validation-------------
    #
    # def is_connected(self):
    #     try:
    #         # Attempt to make a simple HTTP request to check connectivity
    #         response = requests.get('https://www.google.com', timeout=5)
    #         response.raise_for_status()  # Raise an exception for HTTP errors
    #         return True
    #     except requests.RequestException:
    #         return False
    #
    # def show_validation_dialog(self, message):
    #     # Display a dialog for invalid login or sign up
    #     dialog = MDDialog(
    #         text=message,
    #         elevation=0,
    #         buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
    #     )
    #     dialog.open()

    def validate_content(self, tablename):
        extra_info = self.ids.extra_info.text
        extra_info2 = self.ids.extra_info2.text
        District = self.ids.District.text
        State = self.ids.State.text
        pincode = self.ids.pincode.text
        address = self.ids.address.text
        # # Validation logic
        if not extra_info:
            self.ids.extra_info.error = True
            self.ids.extra_info.helper_text = "This field is required."
            self.ids.extra_info.required = True
        elif not extra_info2:
            self.ids.extra_info2.error = True
            self.ids.extra_info2.helper_text = "This field is required."
        elif not State:
            self.ids.State.error = True
            self.ids.State.helper_text = "Please select a state."
            # self.ids.dropdown_state.required = True
        elif not District:
            self.ids.District.error = True
            self.ids.District.helper_text = "Please select a District."
        elif not pincode or len(pincode) != 6:
            self.ids.pincode.error = True
            self.ids.pincode.helper_text = "Invalid pincode (6 digits required)."
            self.ids.pincode.required = True
        elif not address:
            self.ids.address.error = True
            self.ids.address.helper_text = "This field is required."
            self.ids.address.required = True
        else:
            print('validation success')
            self.ids.address.text = ""
            self.ids.District.text = ""
            self.ids.State.text = ""
            self.ids.pincode.text = ""
            self.ids.extra_info.text = ""
            self.ids.extra_info2.text = ""
            print(extra_info)
            print(extra_info2)
            print(State)
            print(District)
            print(pincode)
            print(address)
            print(self.file_data1)
            print(self.file_data2)
            if tablename == 'hospital':
                print('HospitalContent')
                conn = sqlite3.connect("user.db")
                cursor = conn.cursor()
                # Inserting data into the specified table
                cursor.execute(f''' INSERT INTO hospital_table (hospital_name ,established_year , District, State, 
                pincode, address, doc1, doc2) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ''', (extra_info, extra_info2, District,
                                                                                    State, pincode, address,
                                                                                    self.file_data1,
                                                                                    self.file_data2))

                conn.commit()
                conn.close()
                app = MDApp.get_running_app()
                app.root.transition.direction = "down"
                app.root.current = "register_page2"
                return True
            elif tablename == 'mobile_hospital':
                print('MobileCareContent')
                conn = sqlite3.connect("user.db")
                cursor = conn.cursor()
                # Inserting data into the specified table
                cursor.execute(f'''
                        INSERT INTO mobile_hospital_table (vehicle_no, model_year, District, State, pincode, address, doc1, doc2)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (extra_info, extra_info2, District, State, pincode, address, self.file_data1,
                          self.file_data2))

                conn.commit()
                conn.close()
                app = MDApp.get_running_app()
                app.root.transition.direction = "down"
                app.root.current = "register_page2"
                return True

            elif tablename == 'oxi_gym':
                print('GymContent')
                conn = sqlite3.connect("user.db")
                cursor = conn.cursor()
                # Inserting data into the specified table
                cursor.execute(f'''
                        INSERT INTO oxi_gym_table (oxi_gym_name ,established_year , District, State, pincode, address, doc1, doc2)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (extra_info, extra_info2, District, State, pincode, address, self.file_data1,
                          self.file_data2))

                conn.commit()
                conn.close()
                app = MDApp.get_running_app()
                app.root.transition.direction = "down"
                app.root.current = "register_page2"
                return True


# -----------------service-register-form----------------------
class ServiceRegisterForm(MDScreen):
    def __init__(self, **kwargs):
        super(ServiceRegisterForm, self).__init__(**kwargs)


class RegisterPage2(MDScreen):
    dialog = None
    checkbox = None

    def __init__(self, **kwargs):
        super(RegisterPage2, self).__init__(**kwargs)

    def on_checkbox_active(self, checkbox, checkbox_value, add_branch_button):
        self.checkbox = checkbox
        if checkbox_value == 'Hospital':
            print(f"Selected service provider type: {checkbox_value}")
            add_branch_button.disabled = not checkbox.active
        elif checkbox_value == 'Mobile-Hospital':
            print(f"Selected service provider type: {checkbox_value}")
            add_branch_button.disabled = not checkbox.active
        elif checkbox_value == 'Oxi-Gym':
            print(f"Selected service provider type: {checkbox_value}")
            add_branch_button.disabled = not checkbox.active
        else:
            print(f"Selected service provider type: {checkbox_value}")

    # def show_branch_dialog(self, content_type, list_button):
    #
    #     global content_cls, title
    #     if content_type == 'Hospital':
    #         content_cls = HospitalContent()
    #         title = f'Add {content_type}'
    #     elif content_type == 'Mobile-Hospital':
    #         content_cls = MobileCareContent()
    #         title = f'Add {content_type}'
    #     elif content_type == 'Oxi-Gym':
    #         content_cls = GymContent()
    #         title = f'Add {content_type}'
    #     elif content_type == 'Hospital List':
    #         content_cls = HospitalList()
    #         title = content_type
    #     elif content_type == 'Mobile-Hospital List':
    #         content_cls = HospitalList()
    #         title = content_type
    #     elif content_type == 'Oxi-Gym List':
    #         content_cls = HospitalList()
    #         title = content_type
    #     self.dialog = MDDialog(
    #         title=title,
    #         type="custom",
    #         content_cls=content_cls,
    #         padding='0dp',
    #         buttons=[
    #             MDFlatButton(
    #                 text="CANCEL",
    #                 theme_text_color="Custom",
    #                 on_release=self.cancel_dialog,
    #             ),
    #             MDFlatButton(
    #                 text="OK",
    #                 theme_text_color="Custom",
    #                 on_release=lambda x: self.ok_dialog(content_cls, list_button),
    #             ),
    #         ],
    #         auto_dismiss=False,
    #     )
    #
    #     self.dialog.open()
    #     self.update_width()
    def update_width(self, *args):
        if self.dialog:
            # Get the window width
            window_width = Window.width

            # Set the width of the dialog (you can adjust the multiplier as needed)
            self.dialog.width = window_width * 0.8

    def cancel_dialog(self, instance):
        print("CANCEL button clicked")
        self.dialog.dismiss()

    button = None

    def ok_dialog(self, content_cls, list_button):
        self.button = list_button
        print("OK button clicked")
        if content_cls.validate_content():
            print("successful")
            self.checkbox.disabled = True
            self.button.disabled = False
            self.ids.hint_label.text = ""
            self.dialog.dismiss()

    def register_validation(self):
        service_provider_name = self.ids.service_provider_name.text
        service_provider_email = self.ids.service_provider_email.text
        service_provider_password = self.ids.service_provider_password.text
        service_provider_phoneno = self.ids.service_provider_phoneno.text
        service_provider_address = self.ids.service_provider_address.text
        hospital_manager = self.ids.hospital_manager
        mobile_hospital_manager = self.ids.mobile_hospital_manager
        oxigym_manager = self.ids.oxigym_manager
        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        is_valid_password, password_error_message = self.validate_password(service_provider_password)

        if not service_provider_name:
            self.ids.service_provider_name.error = True
            self.ids.service_provider_name.helper_text = "This field is required."
            self.ids.service_provider_name.required = True
        elif not service_provider_email or not re.match(email_regex, service_provider_email):
            self.ids.service_provider_email.error = True
            self.ids.service_provider_email.helper_text = "Invalid email format."
            self.ids.service_provider_email.required = True
        elif not is_valid_password:
            self.ids.service_provider_password.error = True
            self.ids.service_provider_password.helper_text = password_error_message
            self.ids.service_provider_password.required = True
        elif not service_provider_phoneno or len(service_provider_phoneno) != 10:
            self.ids.service_provider_phoneno.error = True
            self.ids.service_provider_phoneno.helper_text = "Invalid phone number (10 digits required)."
            self.ids.service_provider_phoneno.required = True
        elif not service_provider_address:
            self.ids.service_provider_address.error = True
            self.ids.service_provider_address.helper_text = "This field is required."
            self.ids.service_provider_address.required = True
        elif not (hospital_manager.active or mobile_hospital_manager.active or oxigym_manager.active):
            self.ids.hint_label.text = "Please select at least one checkbox"
        elif not (hospital_manager.disabled or mobile_hospital_manager.disabled or oxigym_manager.disabled):
            self.ids.hint_label.text = "Please add values"
        else:
            app = MDApp.get_running_app()
            app.root.transition.direction = "left"
            app.root.current = "login"
            self.ids.service_provider_name.text = ""
            self.ids.service_provider_email.text = ""
            self.ids.service_provider_password.text = ""
            self.ids.service_provider_phoneno.text = ""
            self.ids.service_provider_address.text = ''
            self.ids.hospital_manager.active = False
            self.ids.mobile_hospital_manager.active = False
            self.ids.oxigym_manager.active = False
            self.ids.hint_label.text = ""

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


class HorizontalLineWidget(BoxLayout):
    pass


class HospitalContent(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super(HospitalContent, self).__init__(**kwargs)
        # self.orientation = "vertical"
        # self.size_hint_y = None
        # self.height = "300dp"

    def validate_content(self):
        return super().validate_content(tablename='hospital')


class MobileCareContent(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super(MobileCareContent, self).__init__(**kwargs)
        # self.orientation = "vertical"
        # self.size_hint_y = None
        # self.height = "300dp"

    def validate_content(self):
        return super().validate_content(tablename='mobile_hospital')


class GymContent(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super(GymContent, self).__init__(**kwargs)
        # self.orientation = "vertical"
        # self.size_hint_y = None
        # self.height = "300dp"

    def validate_content(self):
        return super().validate_content(tablename='oxi_gym')


class HospitalListTable(MDScreen):
    def __init__(self, **kwargs):
        super(HospitalListTable, self).__init__(**kwargs)
        self.name = 'list_content'
        # self.orientation = "vertical"
        # self.size_hint_y = None
        # self.height = "300dp"
        initial_data = self.fetch_initial_data()
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.7, "center_x": 0.5},
            size_hint=(.9, None),
            use_pagination=True,
            pagination_menu_pos="center",
            elevation=0,
            padding='0dp',
            check=True,
            column_data=[
                ("Hospital Name", dp(40)),
                ("City", dp(40)),

            ],
            row_data=initial_data,

        )
        self.update_table_height()
        # Creating control buttons.
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5, "center_y": .5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        button_box.add_widget(
            MDRaisedButton(
                text='Delete', on_release=self.on_button_press
            )
        )

        layout = MDFloatLayout()
        layout.add_widget(self.data_tables)
        layout.add_widget(button_box)
        self.add_widget(layout)

    def on_button_press(self, instance_button):
        try:
            {
                "Delete": self.delete_checked_rows,
            }[instance_button.text]()
        except KeyError:
            pass

    def fetch_initial_data(self):
        # Connect to your database and fetch data
        # Replace this with your actual database connection and query logic
        connection = sqlite3.connect('user.db')
        cursor = connection.cursor()

        # Example query: Fetch all rows from the database
        cursor.execute("SELECT hospital_name, District FROM hospital_table")
        db_row_data = cursor.fetchall()

        connection.close()

        return [list(map(str, row)) for row in db_row_data]

    def delete_checked_rows(self):
        def deselect_rows(*args):
            self.data_tables.table_data.select_all("normal")

        checked_rows = self.data_tables.get_row_checks()

        # Connect to the database and delete selected rows
        connection = sqlite3.connect('user.db')
        cursor = connection.cursor()

        for checked_row in checked_rows:
            hospital_name = checked_row[0]  # Assuming hospital_name is the first column
            cursor.execute("DELETE FROM hospital_table WHERE hospital_name=?", (hospital_name,))

        connection.commit()
        connection.close()

        # Remove the deleted rows from the data_tables
        for checked_row in checked_rows:
            if checked_row in self.data_tables.row_data:
                self.data_tables.row_data.remove(checked_row)

        Clock.schedule_once(deselect_rows)
        self.update_table_height()

    def update_table_height(self):
        # Calculate the height of the table based on the number of rows and other parameters
        num_rows = len(self.data_tables.row_data)
        row_height = 40  # Adjust this value based on your row height
        header_height = 60  # Height of the header
        footer_height = 50  # Height of the footer if any
        padding = 10  # Adjust this value based on your padding

        table_height = num_rows * row_height + header_height + footer_height + padding * 2
        self.data_tables.height = table_height

    def validate_content(self):
        return True
