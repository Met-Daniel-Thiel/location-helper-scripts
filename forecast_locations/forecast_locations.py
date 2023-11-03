
import folium
import json
import os
import webbrowser
from folium.features import DivIcon

# Manual input home location info from Gazetteer
# https://github.com/MetOffice/locations-search-pkg-os/tree/master/src/main/resources/gazetteer
c_lat, c_lon= 51.5144361127993, -0.3163454095075852
name = ""

# Create map and add the home location
map_uk = folium.Map(location=[c_lat,c_lon], zoom_start=13)
folium.Marker([c_lat,c_lon], 
              icon=folium.Icon(icon="home",color="red"),
              popup=name,
              ).add_to(map_uk)

# Add all forecast locations within 0.2 lat and 0.3 lon of the home location location
with open('forecast_locations/forecast_locations.json', 'r') as f:
    forecast_locations = json.load(f)

for i in forecast_locations:
    if i['domestic'] == True:
        lat = i['position']['lat']
        lon = i['position']['lon']
        name = i['name']
        
        if (lat < c_lat + 0.2 and lat > c_lat - 0.2 and lon < c_lon + 0.3 and lon > c_lon - 0.3):
            folium.Marker([lat,lon],
                          icon=folium.Icon(icon="info-sign")).add_to(map_uk)
            folium.Marker([lat,lon], 
                icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0),
                            html=f'<div style="font-size: 20pt" <div>{name}</div>',)
                ).add_to(map_uk)
            
# save map and open in a browser
map_uk.save('forecast_locations/map_output_files/forecast_locations_map_uk.html')
webbrowser.open_new(os.path.abspath('forecast_locations/map_output_files/forecast_locations_map_uk.html'))


'''
to add
highlight closest forecast location
find a more slick way getting current/home location
'''