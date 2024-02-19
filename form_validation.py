import os
import sqlite3

from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Creating the hospital_table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_table (
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


class BaseRegistrationScreen(MDScreen):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # extra_info = BooleanProperty(False)
    # extra_info2 = BooleanProperty(False)
    # District = BooleanProperty(False)
    # State = BooleanProperty(False)
    # pincode = BooleanProperty(False)
    # address = BooleanProperty(False)
    #
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     Clock.schedule_interval(self.auto_validate, 0.5)
    #
    # def auto_validate(self, *args):
    #     self.extra_info = bool(self.ids.extra_info.text and len(self.ids.extra_info.text) > 3)
    #     self.extra_info2 = bool(self.ids.extra_info2.text)  # Assuming extra_info2 should not be empty
    #     self.District = bool(self.ids.District.text)
    #     self.State = bool(self.ids.State.text)
    #     self.pincode = bool(
    #         self.ids.pincode.text and len(self.ids.pincode.text) == 6)  # Assuming pincode should be exactly 6 digits
    #     self.address = bool(self.ids.address.text)
    #     self.update_next_button()
    #
    # def all_fields_valid(self):
    #     return all([self.extra_info, self.extra_info2, self.District, self.State, self.pincode, self.address])
    #
    # def update_next_button(self):
    #     self.ids.next_button.disabled = not self.all_fields_valid()
    #
    # def register_validation(self):
    #     if self.all_fields_valid():
    #         # Perform registration process
    #         pass
    #     else:
    #         # Handle invalid fields
    #         pass
    #
    # def on_organization_chane(self, instance, value):
    #     self.extra_info = bool(value)
    #     if not self.extra_info:
    #         self.ids.extra_info.error = True
    #         self.ids.extra_info.helper_text = 'Enter proper name.'
    #     else:
    #         self.ids.extra_info.error = False
    #         self.ids.extra_info.helper_text = ''
    #     self.update_next_button()
    #
    # def on_year_change(self, instance, value):
    #     self.extra_info2 = bool(value)
    #     if not self.extra_info2:
    #         self.ids.extra_info2.error = True
    #         self.ids.extra_info2.helper_text = "Invalid year."
    #     else:
    #         self.ids.extra_info2.error = False
    #         self.ids.extra_info2.helper_text = ''
    #     self.update_next_button()
    #
    # def on_district_change(self, instance, value):
    #     self.District = bool(value)
    #     if not self.District:
    #         self.ids.District.error = True
    #         self.ids.District.helper_text = 'Enter proper district.'
    #     else:
    #         self.ids.District.error = False
    #         self.ids.District.helper_text = ''
    #     self.update_next_button()
    #
    # def on_state_change(self, instance, value):
    #     self.State = bool(value)
    #     if not self.State:
    #         self.ids.State.error = True
    #         self.ids.State.helper_text = "Enter proper state."
    #     else:
    #         self.ids.State.error = False
    #         self.ids.State.helper_text = ''
    #     self.update_next_button()
    #
    # def on_pincode_change(self, instance, value):
    #     self.pincode = bool(value and len(value) == 6)
    #     if not self.pincode:
    #         self.ids.pincode.error = True
    #         self.ids.pincode.helper_text = 'Enter a valid 6-digit pincode.'
    #     else:
    #         self.ids.pincode.error = False
    #         self.ids.pincode.helper_text = ''
    #     self.update_next_button()
    #
    # def on_address_change(self, instance, value):
    #     self.address = bool(value)
    #     if not self.address:
    #         self.ids.address.error = True
    #         self.ids.address.helper_text = 'Enter a proper address.'
    #     else:
    #         self.ids.address.error = False
    #         self.ids.address.helper_text = ''
    #     self.update_next_button()


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
    field_name = None
    file_data1 = None
    file_data2 = None
    file_name1 = None
    file_name2 = None
    path = None

    def file_manager_open(self, field_id):
        self.field_name = field_id
        self.field_id = getattr(self.ids, field_id)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            # use_saf=True,

        )
        self.file_manager.show('/')  # Initial directory when the file manager is opened

    def select_path(self, path):
        if path.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf')):
            self.path = path
            try:
                file_path = path
                if file_path:
                    file_name = os.path.basename(file_path)
                    file_data = self.read_file(file_path)
                    if self.field_name == "file_path":
                        setattr(self.field_id, 'text', file_name)
                        print(file_name)
                        self.file_data1 = file_data
                        self.file_name1 = file_name
                        self.field_id = None
                        # print(self.file_data1)
                    elif self.field_name == "file_path2":
                        setattr(self.field_id, 'text', file_name)
                        self.file_data2 = file_data
                        self.file_name2 = file_name
                        self.field_id = None
                        # print(self.file_data2)
            except:
                msg = "Please select a file."
                setattr(self.field_id, 'text', msg)
            self.file_manager.close()
        else:
            msg = "Please select a JPG, PNG, or PDF file."
            setattr(self.field_id, 'text', msg)
        self.file_manager.close()

    def read_file(self, file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    def exit_manager(self, *args):
        self.file_manager.close()
#-------------------------------validation------------------------------
    # def validate_content(self,classname):
    #     extra_info = self.ids.extra_info.text
    #     extra_info2 = self.ids.extra_info2.text
    #     District = self.ids.District.text
    #     State = self.ids.State.text
    #     pincode = self.ids.pincode.text
    #     address = self.ids.address.text
    #     # # Validation logic
    #     if not extra_info:
    #         self.ids.extra_info.error = True
    #         self.ids.extra_info.helper_text = "This field is required."
    #         self.ids.extra_info.required = True
    #     elif not extra_info2:
    #         self.ids.extra_info2.error = True
    #         self.ids.extra_info2.helper_text = "This field is required."
    #     elif not State:
    #         self.ids.State.error = True
    #         self.ids.State.helper_text = "Please select a state."
    #         # self.ids.dropdown_state.required = True
    #     elif not District:
    #         self.ids.District.error = True
    #         self.ids.District.helper_text = "Please select a District."
    #     elif not pincode or len(pincode) != 6:
    #         self.ids.pincode.error = True
    #         self.ids.pincode.helper_text = "Invalid pincode (6 digits required)."
    #         self.ids.pincode.required = True
    #     elif not address:
    #         self.ids.address.error = True
    #         self.ids.address.helper_text = "This field is required."
    #         self.ids.address.required = True
    #     else:
    #         print('validation success')
    #         self.ids.address.text = ""
    #         self.ids.District.text = ""
    #         self.ids.State.text = ""
    #         self.ids.pincode.text = ""
    #         self.ids.extra_info.text = ""
    #         self.ids.extra_info2.text = ""
    #         print(extra_info)
    #         print(extra_info2)
    #         print(State)
    #         print(District)
    #         print(pincode)
    #         print(address)
    #         print(self.file_data1)
    #         print(self.file_data2)
    #
    #
    #         conn = sqlite3.connect("users.db")
    #         cursor = conn.cursor()
    #         # Inserting data into the specified table
    #         cursor.execute(f''' INSERT INTO service_table (hospital_name ,established_year , District, State,
    #         pincode, address, doc1, doc2) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ''', (extra_info, extra_info2, District,
    #                                                                             State, pincode, address,
    #                                                                             self.file_data1,
    #                                                                             self.file_data2))
    #
    #         conn.commit()
    #         conn.close()
    #         if classname=='oxiclinic':
    #             self.manager.push("service_hospital_doc")
    #         elif classname=='oxitaxi':
    #             self.manager.push("service_mobile_hospital_doc")
    #         elif classname=='oxigym':
    #             self.manager.push("service_oxygym_doc")

