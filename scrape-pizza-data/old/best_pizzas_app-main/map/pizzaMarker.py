# from map.locationpopupmenu import LocationPopupMenu
# from locationpopupmenu import LocationPopupMenu
from kivy_garden.mapview import MapMarkerPopup

class PizzaMarker(MapMarkerPopup):
    # source = "pizza_marker.png"
    pizza_data = []

    

    def on_release(self):
        # Open up the locationPopupMenu
        # LocationPopupMenu(self.pizza_data)
        pass
