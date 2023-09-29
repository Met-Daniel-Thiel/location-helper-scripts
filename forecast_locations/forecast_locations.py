
import folium
import json
import os
import webbrowser

# Manual input location info from Gazetteer
# https://github.com/MetOffice/locations-search-pkg-os/tree/master/src/main/resources/gazetteer
c_lon = -0.4
c_lat = 51.67
name = "North Watford"

# Create basic map and add the gazetteer location
map_uk = folium.Map(location=[c_lat,c_lon], zoom_start=14)
folium.Marker([c_lat,c_lon], 
              icon=folium.Icon(icon="home",color="red"),
              popup=name,
              ).add_to(map_uk)

# Add all forecast locations within 0.2 lat and 0.2 lon of the gazetteer location
with open('forecast_locations/forecast_locations.json', 'r') as f:
    forecast_locations = json.load(f)


for i in forecast_locations:
    if i['domestic'] == True:
        lat = i['position']['lat']
        lon = i['position']['lon']
        name = i['name']
        
        if (lat < c_lat + 0.2 and lat > c_lat - 0.2 and lon < c_lon + 0.2 and lon > c_lon - 0.2):
            folium.Marker([lat,lon], 
                          popup=f"Forcast Location: {name}",
                          icon=folium.Icon(icon="info-sign")).add_to(map_uk)
            
# save map and open in a browser
map_uk.save('forecast_locations/map_output_files/forecast_locations_map_uk.html')
webbrowser.open_new(os.path.abspath('forecast_locations/map_output_files/forecast_locations_map_uk.html'))