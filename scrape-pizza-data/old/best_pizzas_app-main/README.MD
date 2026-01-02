This folder concerns creating apps that will show you the best Neapolitan pizza in the world. 

Data comes from the official site: https://www.50toppizza.it/

Currently a Jupyter notebook is created, the app developed in the Kivy framework is still work in progress.

Repo content:
Step 1: ./scraper/web_scraper_tool.py
    Scrape all the information concerning the best pizza in the world and store it in the JSON text format

Step 2: ./geoloc/google_maps_platform.ipynb
    Get the geolocation of the pizza places via the Google Developers Platform with an API key

Step 3: ./pizza data/JSON_to_db.ipynb
    Store all data from the JSON file (incl updated geolocation info) to a db file as an excerise to later be used in the Kivy app

Step 4: .map/list_to_map.ipynb
    Show markers of the best pizza place (with ranking and name) on a map using Folium.
    Run each code block to make it work.

Step 5: TODO
    create an app in the Kivy framework

Step 6: TODO
    Compile and create an android .apk file with menu

