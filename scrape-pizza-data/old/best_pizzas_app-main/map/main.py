from kivymd.app import MDApp
from pizzaMapView import PizzaMapView
import sqlite3 

class MainApp(MDApp):
    connection = None
    cursor = None

    def on_start(self):
        # Initialize GPS

        # Connect to database
        self.connection = sqlite3.connect('C:\programming\Code\pizza map\pizza data\IT_pizza_data.db')
        self.cursor = self.connection.cursor()

        # Instantiate SearchPopupMenu

MainApp().run()