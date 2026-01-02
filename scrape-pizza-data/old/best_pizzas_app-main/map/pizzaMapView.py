from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
from kivy_garden.mapview.view import MapMarkerPopup
from pizzaMarker import PizzaMarker

class PizzaMapView(MapView):
    getting_pizza_timer = None
    pizza_names = []

    def start_getting_pizza_in_fov(self):
        # after 0.5 second, get the pizza places in the field of view
        try:
            self.getting_pizza_timer.cancel()
        except:
            pass

        self.getting_pizza_timer = Clock.schedule_once(self.get_pizza_in_fov, 0.5)

    def get_pizza_in_fov(self, *args):
        # Get reference to main app and the dartabase cursor
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        app = App.get_running_app()
        sql_statement = """
            SELECT * 
            FROM pizza 
            WHERE lat > %s AND lat < %s 
            AND lon > %s AND lon < %s;
            """%(min_lat, max_lat, min_lon, max_lon)

        app.cursor.execute(sql_statement)
        pizzas = app.cursor.fetchall()
        print(pizzas)
        for pizza in pizzas:  
            name = pizza[1]
            if name in self.pizza_names:
                continue
            self.add_pizza(pizza)

    def add_pizza(self, pizza):
        # create the pizza marker
        lat, lon = pizza[5], pizza[6]

        marker = PizzaMarker(lat=float(lat), lon=float(lon), source='pizza_marker_small.png')
        marker.pizza_data = pizza

        # Add the pizza marker to the map
        self.add_widget(marker)

        # Keep track of the marker's name
        name = pizza[1]
        self.pizza_names.append(name)