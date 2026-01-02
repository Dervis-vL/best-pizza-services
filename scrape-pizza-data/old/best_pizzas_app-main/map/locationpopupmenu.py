from kivymd.uix.dialog import MDListDialog

class LocationPopupMenu(MDListDialog):

    def __init__(self, pizza_data):
        super().__init__()
        
        # Set all of the fields of pizza data
