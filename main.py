import sqlite3
from datetime import date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class SurveyApp(App):
    def build(self):
        self.init_db()
    
        layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        self.name_input = TextInput(hint_text="Enter patient's name: ")
        layout.add_widget(self.name_input)

        self.age_input = TextInput(hint_text="Enter patient's age:")
        layout.add_widget(self.age_input)

        self.village_input = TextInput(hint_text='Enter village name: ')
        layout.add_widget(self.village_input)

        self.phoneno_input = TextInput(hint_text="Enter patient's phone number: ")
        layout.add_widget(self.phoneno_input)

        self.bp_input = TextInput(hint_text="Enter patient's Blood Pressure: ")
        layout.add_widget(self.bp_input)

        self.weight_input = TextInput(hint_text="Enter patient's weight: ")
        layout.add_widget(self.weight_input)

        self.sc_input = TextInput(hint_text="Are patient's symptoms normal: ")
        layout.add_widget(self.sc_input)

        self.vc_input = TextInput(hint_text='Vaccine given to patient: ')
        layout.add_widget(self.vc_input)

        self.date_input = TextInput(hint_text='Enter date of administration: ')
        layout.add_widget(self.date_input)

        self.ndd_input = TextInput(hint_text='Enter next due date: ')
        layout.add_widget(self.ndd_input)

        submit_btn = Button(text='Submit')
        submit_btn.bind(on_press=self.save_data)
        layout.add_widget(submit_btn)

        self.count_label = Label(text="Entries submitted today: 0")
        layout.add_widget(self.count_label)
        
        return layout
    
    def init_db(self):
        self.conn = sqlite3.connect("survey.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS survey (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age TEXT,
                village TEXT,
                phoneno TEXT,
                bp TEXT,
                weight TEXT,
                sc TEXT,
                vc TEXT,
                date TEXT,
                ndd TEXT
            )
        """)
        self.conn.commit()
   
    def show_all_entries(self):
        self.cursor.execute("SELECT * FROM survey")
        rows = self.cursor.fetchall()
        for row in rows:
         print(row)

    def save_data(self, instance):
        today = date.today().isoformat()
        
        self.cursor.execute("""
            INSERT INTO survey (name, age, village, phoneno, bp, weight, sc, vc, date, ndd)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
         self.name_input.text,
         self.age_input.text,
         self.village_input.text,
         self.phoneno_input.text,
         self.bp_input.text,
         self.weight_input.text,
         self.sc_input.text,
         self.vc_input.text,
         today,
         self.ndd_input.text
    ))
        self.show_all_entries()
        self.conn.commit()

        self.cursor.execute("SELECT COUNT(*) FROM survey WHERE date = ?", (today,))
        count = self.cursor.fetchone()[0]

        self.count_label.text = f"Entries submitted today: {count}"
        print(f"✅ Entry saved. Total today: {count}")

SurveyApp().run()
