import folium
import os
import webbrowser
import requests
from folium.features import DivIcon
from geopy.distance import geodesic 
from geopy import Nominatim

######################################################################################################
home_location = "Kenton, Devon"     # Any location name, postcode or cordinates as a string
location_count = 100    # Number of forecast locations to be displayed on map (must be at least one)
######################################################################################################

# Get forecast locations from LocsMan
print("Retrieving current forecast locations from LocsMan")
locs_man_url = "https://www.metoffice.gov.uk/public/data/services/locations/v3"
response = requests.get(locs_man_url)
if response.status_code == 200:     
    forecast_locations_locs = response.json()   
    print(f"Retrieved {len(forecast_locations_locs)} locations from LocsMan")      
else:     
    print(f"Failed to fetch data. Status code: {response.status_code}")
    exit()

# get cordinates for home location
geocoder = Nominatim(user_agent="Captain Dan")
location_raw = geocoder.geocode(home_location)
try:
    print(f"Found location data for: {location_raw.address}")
except AttributeError:
    print(f'### Sorry. "{home_location}" could not be found. Please check for spelling/errors')
    exit()

home_lat, home_long = location_raw.latitude, location_raw.longitude

# Create map and add the home location
forecast_locations_map = folium.Map(location=[home_lat,home_long], zoom_start=12)
folium.Marker([home_lat,home_long], icon=folium.Icon(icon="home",color="red")).add_to(forecast_locations_map)
folium.Marker([home_lat,home_long], icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0), html=f'<div style="font-size: 15pt" <div>{home_location}</div>',)).add_to(forecast_locations_map)
   
# Generate dictionary of closest forecast locations
closest_forecast_locations = {100000:""} # initilise no empty dictionary 

for forecast_location in forecast_locations_locs:
    distance = geodesic((home_lat, home_long), (forecast_location['position'])).km
    
    if distance < max(list(closest_forecast_locations.keys())):
        closest_forecast_locations[distance] = forecast_location
        if len(closest_forecast_locations) > location_count:
            closest_forecast_locations.pop(max(list(closest_forecast_locations.keys())))
        
# populate map with forecast locations
for closest_forecast_location in closest_forecast_locations:
    lat, long = closest_forecast_locations[closest_forecast_location]["position"]
    name = closest_forecast_locations[closest_forecast_location]["name"]
    distance = round(closest_forecast_location,1)  

    folium.Marker([lat,long], icon=DivIcon(icon_size=(250,30),icon_anchor=(0,0), 
                                           html=f'<div style="font-size: 15pt" <div>{name} {distance}km</div>',)
                                           ).add_to(forecast_locations_map)

    folium.Marker([lat,long], icon=folium.Icon(color='blue',icon="sun", prefix='fa'),
                  popup=f'''<div style="font-size: 15pt"; "background-color: white, >
                  Name:{name}<br>
                  Country:{closest_forecast_locations[closest_forecast_location]["locationMetadata"]["country"]}<br>
                  UnitaryAuthority:{closest_forecast_locations[closest_forecast_location]["locationMetadata"]["unitaryAuthority"]}<br>
                  FloodRegion:{closest_forecast_locations[closest_forecast_location]["locationMetadata"]["floodRegion"]}<br>
                  LocationType:{closest_forecast_locations[closest_forecast_location]["locationType"]}<br>
                  Altitude:{closest_forecast_locations[closest_forecast_location]["locationMetadata"]["altitude"]}<br>
                  Postition:{lat}, {long}<br>
                  GeoHash:{closest_forecast_locations[closest_forecast_location]["geohash"]}<br>
                  SSPAID:{closest_forecast_locations[closest_forecast_location]["sspaId"]}<br>
                  NearestClimateData_SSPAID:{closest_forecast_locations[closest_forecast_location]["locationClimateData"]["nearestClimateSSPAId"]}<br>
                  NearestObservationData_SSPAID:{closest_forecast_locations[closest_forecast_location]["locationObservationData"]["nearestObservationSSPAId"]}
                  </div>'''
                  ).add_to(forecast_locations_map)
    
# Draw line between search location and closest location
closest = closest_forecast_locations[min(list(closest_forecast_locations.keys()))]
folium.PolyLine(locations = [[home_lat, home_long], closest['position']], color='red', weight=10, opacity=0.5
                ).add_to(forecast_locations_map)

# save map and open in a browser
forecast_locations_map.save('data/maps/forecast_locations_map_uk.html')
webbrowser.open_new(os.path.abspath('data/maps/forecast_locations_map_uk.html'))

'''
TODO
- error handling for bad/miss-spelled location names and locations not in UK
'''
