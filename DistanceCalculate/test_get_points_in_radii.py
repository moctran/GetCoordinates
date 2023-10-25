import pandas as pd
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

# Load data from the CSV file
csv_file = '/Users/moctran/Desktop/HUST/LabDrone/Multi-objective_truck_drone/TestGenerator/GetCoordinates/results.csv' 
data = pd.read_csv(csv_file)

# Define a function to calculate haversine distance
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

# Calculate x and y coordinates for all data points based on latitude and longitude
data['x'] = data.apply(lambda row: haversine(data['Latitude'].mean(), data['Longitude'].mean(), row['Latitude'], data['Longitude'].mean()), axis=1)
data['y'] = data.apply(lambda row: haversine(data['Latitude'].mean(), data['Longitude'].mean(), data['Latitude'].mean(), row['Longitude']), axis=1)

# Calculate the centroid based on x and y coordinates
centroid_x = data['x'].mean() + 2
centroid_y = data['y'].mean() + 2

# Define radii in kilometers
radii = [2, 5, 10]

# Create DataFrames for points within each radius
points_in_2km = pd.DataFrame()
points_in_5km = pd.DataFrame()
points_in_10km = pd.DataFrame()

# Calculate the number of points within each radius and save to separate DataFrames
for i, radius in enumerate(radii):
    for index, row in data.iterrows():
        distance_to_centroid = ((row['x'] - centroid_x) ** 2 + (row['y'] - centroid_y) ** 2) ** 0.5
        if distance_to_centroid <= radius:
            if radius == 2:
                points_in_2km = points_in_2km.append(row[['Latitude', 'Longitude']])
            elif radius == 5:
                points_in_5km = points_in_5km.append(row[['Latitude', 'Longitude']])
            elif radius == 10:
                points_in_10km = points_in_10km.append(row[['Latitude', 'Longitude']])

# Save points within each radius to separate CSV files
points_in_2km.to_csv('points_within_2km.csv', index=False)
points_in_5km.to_csv('points_within_5km.csv', index=False)
points_in_10km.to_csv('points_within_10km.csv', index=False)

plt.show()
