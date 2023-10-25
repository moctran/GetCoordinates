import requests
import urllib.parse
import pandas as pd

# Read addresses from text file 
with open('circleK2.txt') as f:
  addresses = f.readlines()

# Remove newline chars  
addresses = [x.strip() for x in addresses] 

# API key
api_key = "AIzaSyB6nspanN80JOGinGmBMhhAlTAFUa3wjo0"

# Lists to store data
lats, lngs, results = [], [], [] 

# Loop through addresses
for address in addresses:

  # Encode address
  url_address = urllib.parse.quote(address)
  
  # Geocoding API request
  url = f"https://maps.googleapis.com/maps/api/geocode/json?address={url_address}&key={api_key}"
  
  # Get JSON response 
  response = requests.get(url)
  data = response.json()

  # Get lat, lng
  if data['status'] == 'OK':
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    lats.append(lat)
    lngs.append(lng)
    results.append(address)

# Create dataframe  
df = pd.DataFrame({'Address': results,
                   'Latitude': lats,
                   'Longitude': lngs})
                   
# Write to Excel file
df.to_excel('results_ck.xlsx', index=False)

print('Geocoding done!')

try:
  response = requests.get(url)
except requests.exceptions.ConnectionError as err:
  print("Error getting geocode from API: ", err)