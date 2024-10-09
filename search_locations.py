'''
Places the results for the website or app location search on a map and indicates forecast locations
'''

import requests 
import folium
from folium.features import DivIcon
import webbrowser
import os
import json
from geopy.distance import geodesic

# inputs
search_term = "Exeter"    # search term
results = 100   # number of resaults. (app/pw return 5, max 100

# construct and make request
url = 'https://www.metoffice.gov.uk/plain-rest-services/location-search' 
params = {'searchTerm': search_term,'max': results,'filter': 'exclude-marine-offshore'} 
response = requests.get(url, params=params) 
if response.status_code == 200:     
    search_locations = response.json()   
    print(f" retrieved {len(search_locations)} locations")      
else:     
    print(f"Failed to fetch data. Status code: {response.status_code}")

# import forecast locations
with open('data/forecast_locations.json', 'r') as f:
    forecast_locations = json.load(f)

# Create map and center on the UK
search_locations_map = folium.Map(location=[54.67846033848346, -4.358720420417081], zoom_start=7)

# add locations to map
locations_added={}
for location in search_locations:
    folium.Marker([location['latLong'][0],location['latLong'][1]], 
                icon=folium.Icon(color='red',icon="user", prefix='fa'),
                popup=f'<div style="font-size: 20pt"; "background-color: white, >Name:{location["name"]}<br>Area:{location["area"]}<br>Type:{location["type"]}<br>Geohash:{location["geohash"]}<br>NearestGeohash:{location["nearestGeohash"]}</div>'
                ).add_to(search_locations_map)
    folium.Marker([location['latLong'][0],location['latLong'][1]], 
                  icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0),
                               html=f'<div style="font-size: 20pt"; "background-color: white, >{location["name"]}</div>')
                  ).add_to(search_locations_map)   
    locations_added[location["geohash"]] = {"lat":location['latLong'][0], "long":location['latLong'][1]}
    
    # add related forecast location to map if not already present
    if location["nearestGeohash"] not in locations_added.keys():
        for location in forecast_locations:
            if location["nearestGeohash"] == location["geohash"]:
                lat, long, name = location['position']['lat'], location['position']['lon'], location["name"]
                folium.Marker([lat,long], icon=folium.Icon(color='blue',icon="sun", prefix='fa'),
                              popup=f'<div style="font-size: 20pt"; "background-color: white, >Name:{location["name"]}<br>Area:{location["metadata"]["unitary_authority"]}<br>Geohash:{location["geohash"]}</div>'
                              ).add_to(search_locations_map)
                folium.Marker([lat,long], icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0), html=f'<div style="font-size: 20pt" <div>{name}</div>',)).add_to(search_locations_map)
                locations_added[location["geohash"]] = {"lat":location['position']['lat'], "long":location['position']['lon']}
                break

    # draw line between seach location and forecast location
    lat_1 = locations_added[location['geohash']]['lat']
    long_1 = locations_added[location['geohash']]['long']
    lat_2 = locations_added[location['nearestGeohash']]['lat']
    long_2 = locations_added[location['nearestGeohash']]['long']
    distance = round(geodesic((lat_1, long_1), (lat_2,long_2)).km,1)
    folium.PolyLine(locations = [[lat_1, long_1], [lat_2, long_2]],  
                        color='red', weight=10, opacity=0.5,
                        popup=f"{distance} km").add_to(search_locations_map)




# save map and open in a browser
search_locations_map.save('data/maps/search_locations_map.html')
webbrowser.open_new(os.path.abspath('data/maps/search_locations_map.html'))