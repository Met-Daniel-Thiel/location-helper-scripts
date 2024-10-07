
import folium
import json
import os
import webbrowser
from folium.features import DivIcon
from geopy.distance import geodesic 
from geopy import Nominatim

# Input any Location name or Postcode, also number of forecast locations to be shown
location = "Brendon"
location_count = 10

# get cords for location
geocoder = Nominatim(user_agent="capt dan")
location_raw = geocoder.geocode(location)
c_lat, c_long = location_raw.latitude, location_raw.longitude

# Create map and add the home location
map_uk = folium.Map(location=[c_lat,c_long], zoom_start=12)
folium.Marker([c_lat,c_long], icon=folium.Icon(icon="home",color="red")).add_to(map_uk)
folium.Marker([c_lat,c_long], icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0), html=f'<div style="font-size: 20pt" <div>{location}</div>',)).add_to(map_uk)

# find closest forecast locations
with open('forecast_locations_data/forecast_locations.json', 'r') as f:
    forecast_locations = json.load(f)

# find the closest 10 forecast locations
closest_locations = {100:""} # initilise dictionary, must have at least one key so will never produce an empty list of keys 
for i in forecast_locations:
    if i['domestic'] == True:
        lat, long = i['position']['lat'], i['position']['lon']
        distance = geodesic((c_lat, c_long), (lat, long)).km
        
        if distance < max(list(closest_locations.keys())):
            closest_locations[distance] = {"name":i['name'], "lat":lat, "long":long}
            if len(closest_locations) > location_count:
                closest_locations.pop(max(list(closest_locations.keys())))
        
# populate map
for l in closest_locations:
    name = closest_locations[l]["name"]
    lat = closest_locations[l]["lat"]
    long = closest_locations[l]["long"]

    folium.Marker([lat,long], icon=folium.Icon(icon="info-sign")).add_to(map_uk)
    folium.Marker([lat,long], icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0), html=f'<div style="font-size: 20pt" <div>{name}</div>',)).add_to(map_uk)

# Draw line between search location and closest location
closest = closest_locations[min(list(closest_locations.keys()))]
folium.PolyLine(locations = [[c_lat, c_long], [closest['lat'],closest['long']]],  
                        color='red', weight=10, opacity=0.5,
                        popup='Closest').add_to(map_uk)


# save map and open in a browser
map_uk.save('forecast_locations_data/map_output_files/forecast_locations_map_uk.html')
webbrowser.open_new(os.path.abspath('forecast_locations_data/map_output_files/forecast_locations_map_uk.html'))





