import sqlite3

from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen

from ServiceRegister import HospitalListTable


class ServicesList(MDScreen):
    def __init__(self, **kwargs):
        super(HospitalListTable, self).__init__(**kwargs)
        self.name = 'list_content'
        # self.orientation = "vertical"
        # self.size_hint_y = None
        # self.height = "300dp"
        initial_data = self.fetch_initial_data()
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(.9, .6),
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
        # Creating control buttons.
        button_box = MDBoxLayout(
            pos_hint={"center_x": 1, 'center_y': .2},
            size_hint=(.9, .2),
            padding="14dp",
            spacing="14dp",
        )

        button_box.add_widget(
            MDRectangleFlatButton(
                text='Delete',
                on_release=self.on_button_press,
                pos_hint={"center_y": .5},

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

    def update_table_height(self):
        # Calculate the height of the table based on the number of rows and other parameters
        num_rows = len(self.data_tables.row_data)
        row_height = 40  # Adjust this value based on your row height
        header_height = 60  # Height of the header
        footer_height = 50  # Height of the footer if any
        padding = 10  # Adjust this value based on your padding

        table_height = num_rows * row_height + header_height + footer_height + padding * 2
        self.data_tables.height = table_height