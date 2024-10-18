# README #

### What is this repository for? ###
Helper scripts to assist with visulising and troubshooting location based issues with the app and public website.

** Script: nearest_forecast_locations.py
* What does it do?
Produces a map showing the nearest forecast locations to a search location.
The distance to each forecast location is shown in km, with the option to left click on a forecast location for more information.

* How to use it?
Change the values for home_location and location_count as required, then run the script.
home location - the location whos nearest forcast locations you want to find. This can be a town/city name, postcode or coordinates in the form of a string.
location_count - the number of forecast locations you want to display.


** Script: search_locations.py
Still in development









### How do I get set up? ###


Dependencies
* Dependencies are contained within requirements.txt
* run [pip install -r requirements.txt] to install all required dependencies.

### How does it work?
Run the python file that corresponds to the report that you are looking to generate. 

akamai_report_for_datapoint
the script will pull the daily Akamai bytes_by_url reports from Akamai via the API, process them and output an excell file which is saved localy in the users downloads folder.
IMPORTANT! Akamai reports run several days behind. If some of the data is not yet avaiable the report will still be generated with the available data. The console output will confirm which days data have been downloaded.

### Who do I talk to? ###
daniel.thiel@metoffice.gov.uk









icons https://fontawesome.com/v4/icons/