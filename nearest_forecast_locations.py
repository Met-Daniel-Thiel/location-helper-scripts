'''
Places all the nearest forecast locations to a given location on a map and draws a line indicating the closest
'''

import folium
import json
import os
import webbrowser
from folium.features import DivIcon
from geopy.distance import geodesic 
from geopy import Nominatim

# Input any location name or postcode or cordinates as string
# Input number of forecast locations to be shown as int
location = "Newtown"
location_count = 100

# get cordinates for location
geocoder = Nominatim(user_agent="capt dan")
location_raw = geocoder.geocode(location)
home_lat, home_long = location_raw.latitude, location_raw.longitude

# Create map and add the home location
forecast_locations_map = folium.Map(location=[home_lat,home_long], zoom_start=12)
folium.Marker([home_lat,home_long], icon=folium.Icon(icon="home",color="red")).add_to(forecast_locations_map)
folium.Marker([home_lat,home_long], icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0), html=f'<div style="font-size: 20pt" <div>{location}</div>',)).add_to(forecast_locations_map)

# import forecast locations
with open('data/forecast_locations.json', 'r') as f:
    forecast_locations = json.load(f)

# find the closest 10 forecast locations
closest_locations = {100:""} # initilise dictionary, must have at least one key so will never produce an empty list of keys 
for location in forecast_locations:
    if location['domestic'] == True:
        lat, long = location['position']['lat'], location['position']['lon']
        area, geohash = location["metadata"]["unitary_authority"], location["geohash"]
        distance = geodesic((home_lat, home_long), (lat, long)).km
        
        if distance < max(list(closest_locations.keys())):
            closest_locations[distance] = {"name":location['name'], "lat":lat, "long":long, "area":area, "geohash":geohash}
            if len(closest_locations) > location_count:
                closest_locations.pop(max(list(closest_locations.keys())))
        
# populate map
for closest_location in closest_locations:
    name, area = closest_locations[closest_location]["name"], closest_locations[closest_location]["area"]
    lat, long = closest_locations[closest_location]["lat"], closest_locations[closest_location]["long"]
    geohash = closest_locations[closest_location]["geohash"]
    distance = round(closest_location,1)

    folium.Marker([lat,long], icon=folium.Icon(color='blue',icon="sun", prefix='fa'),
                popup=f'<div style="font-size: 20pt"; "background-color: white, >Name:{name}<br>Area:{area}<br>Geohash:{geohash}</div>'
                ).add_to(forecast_locations_map)
    folium.Marker([lat,long], icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0), html=f'<div style="font-size: 20pt" <div>{name} {distance}km</div>',)).add_to(forecast_locations_map)

# Draw line between search location and closest location
closest = closest_locations[min(list(closest_locations.keys()))]
distance = round(geodesic((home_lat, home_long), (closest['lat'],closest['long'])).km,1)
folium.PolyLine(locations = [[home_lat, home_long], [closest['lat'],closest['long']]],  
                        color='red', weight=10, opacity=0.5).add_to(forecast_locations_map)


# save map and open in a browser
forecast_locations_map.save('data/maps/forecast_locations_map_uk.html')
webbrowser.open_new(os.path.abspath('data/maps/forecast_locations_map_uk.html'))




'''
TODO
- error handling for bad/miss-spelled location names and locations not in UK
- requirements.txt
- readme
- update sorce for forecast locations
'''
