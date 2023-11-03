import requests 
import folium
from folium.features import DivIcon
import webbrowser
import os

url = 'https://www.metoffice.gov.uk/plain-rest-services/location-search' 
params = {
    'searchTerm': 'kew',
    'max': 20,
    'filter': 'exclude-marine-offshore' 
    } 

response = requests.get(url, params=params) 

if response.status_code == 200:     
    data = response.json()         
else:     
    print(f"Failed to fetch data. Status code: {response.status_code}")

# Create map and add the home location
map_uk = folium.Map(location=[54.67846033848346, -4.358720420417081], zoom_start=7)

# add locations to map
for l in data:
    folium.Marker([l['latLong'][0],l['latLong'][1]], 
                icon=folium.Icon(icon="home",color="red")).add_to(map_uk)
    folium.Marker([l['latLong'][0],l['latLong'][1]], 
                  icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0),
                               html=f'<div style="font-size: 20pt"; "background-color: white, >name: {l["name"]}<br>area: {l["area"]}<br>nearestGeohash: {l["nearestGeohash"]}<br>geohash: {l["geohash"]}</div>',)
                  ).add_to(map_uk)

# save map and open in a browser
map_uk.save('search_locations/map_output_files/forecast_locations_map_uk.html')
webbrowser.open_new(os.path.abspath('search_locations/map_output_files/forecast_locations_map_uk.html'))