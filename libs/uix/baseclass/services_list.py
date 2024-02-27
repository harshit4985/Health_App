import sqlite3
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import rgba
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDFlatButton, MDRoundFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class ServicesList(MDScreen):

    def __init__(self, **kwargs):
        super(ServicesList, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)
        self.name = 'list_content'
        self.load_data()
    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            self.on_back_button()
            return True
        return False

    def on_back_button(self):
        self.manager.push_replacement("main_sc", "right")

    def on_pre_enter(self):
        self.load_data()

    def load_data(self):
        initial_data = self.fetch_initial_data()
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(1, .7),
            use_pagination=True,
            pagination_menu_pos="center",
            elevation=0,
            padding='0dp',
            check=True,
            column_data=[
                ("Organization Name", dp(45)),
                ("City", dp(30)),
            ],
            row_data=initial_data,
        )

        # Creating control buttons.
        button_box = MDBoxLayout(
            pos_hint={"center_x": 1.2, 'center_y': .15},
            size_hint=(.9, .2),
            padding="14dp",
            spacing="14dp",
        )

        button_box.add_widget(
            MDIconButton(
                icon='trash-can-outline',
                text='Delete',
                on_release=self.on_button_press,
            )
        )
        button_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(60),
            padding=dp(10),
            spacing=dp(10)
        )

        confirm_button = MDRoundFlatButton(
            text="CONFIRM",
            size_hint=(0.5, None),
            height=dp(40),
            pos_hint={'center_x': .5, 'center_y': .5},
            md_bg_color=(1, 0, 0, 1),
            font_name="Roboto-Bold",
            valign="center",
            text_color=(1, 1, 1, 1),
            theme_text_color="Custom",
            line_color = (0, 0, 0, 0),
            on_release=self.confirm_action
        )
        label = MDLabel(
            text="Organization List ",
            font_name="Roboto-Bold",
            pos_hint={"center_y": .9},
            size_hint_y=.1,
            font_size="20sp",
            font_style='H6',
            halign='center')
        button_layout.add_widget(confirm_button)
        layout = MDFloatLayout(
            MDIconButton(
                icon="arrow-left",
                pos_hint={"center_y": .95},
                user_font_size="30sp",
                size_hint_y=.15,
                theme_text_color="Custom",
                on_release=self.back,
                text_color=rgba(26, 24, 58, 255), ),

        )
        layout.add_widget(self.data_tables)
        layout.add_widget(button_layout)
        layout.add_widget(button_box)
        layout.add_widget(label)
        self.clear_widgets()
        self.add_widget(layout)

    def back(self, instance):
        self.manager.push_replacement("service_register_form2", "right")

    def confirm_action(self, instance):
        print("Confirmation button pressed")
        self.manager.push_replacement("service_register_form2", "right")

    def on_button_press(self, instance_button):
        try:
            {
                "Delete": self.delete_checked_rows,
            }[instance_button.text]()
        except KeyError:
            pass

    def fetch_initial_data(self):
        # Connect to your database and fetch data
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        # Example query: Fetch all rows from the database
        cursor.execute("SELECT organization_name, District FROM service_table")
        db_row_data = cursor.fetchall()

        connection.close()

        return [list(map(str, row)) for row in db_row_data]

    def delete_checked_rows(self):
        def deselect_rows(*args):
            self.data_tables.table_data.select_all("normal")

        checked_rows = self.data_tables.get_row_checks()

        # Connect to the database and delete selected rows
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        for checked_row in checked_rows:
            organization_name = checked_row[0]  # Assuming hospital_name is the first column
            cursor.execute("DELETE FROM service_table WHERE organization_name=?", (organization_name,))

        connection.commit()
        connection.close()

        # Remove the deleted rows from the data_tables
        for checked_row in checked_rows:
            if checked_row in self.data_tables.row_data:
                self.data_tables.row_data.remove(checked_row)

        Clock.schedule_once(deselect_rows)
