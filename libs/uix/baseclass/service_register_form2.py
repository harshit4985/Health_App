import re

from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class HorizontalLineWidget(MDBoxLayout):
    pass


class ServiceRegisterForm2(MDScreen):
    def __init__(self, **kwargs):
        super(ServiceRegisterForm2, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)
    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            self.on_back_button()
            return True
        return False

    def on_back_button(self):
        self.manager.push_replacement("service_register_form1", "right")
    def register(self):
        print("registered")
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        screen_to_clear = self.manager.get_screen(classname)
        data = screen_to_clear.form_data()
        if doc1 is not None and doc2 is not None:
            data.append(doc1)
            data.append(doc2)
            self.file_data1 = None
            self.file_name1 = None
            self.ids.file_path.text = 'None selected'

            self.file_data2 = None
            self.file_name2 = None
            self.ids.file_path2.text = 'None selected'

            # print("Data:", data)

            try:
                cursor.execute('''
                        INSERT INTO oxiclinicservice (oxiclinic_name, established_year, District, State, pincode, address, capsules, doc1, doc2) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
                conn.commit()
                print("Data inserted successfully")  # Print success message
            except sqlite3.Error as e:
                print("Error inserting data:", e)
                conn.rollback()
            self.manager.push_replacement("service_register_form2", "right")
            self.ids.hint_label.text = " "
            if screen_to_clear:
                screen_to_clear.reset_fields()
        else:
            self.ids.hint_label.text = "Both documents are required"
        cursor.close()
        conn.close()