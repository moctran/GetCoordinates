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

# Initialize counts for points within each radius
points_within_radius = [0] * len(radii)

# Calculate the number of points within each radius
for i, radius in enumerate(radii):
    for _, row in data.iterrows():
        distance_to_centroid = ((row['x'] - centroid_x) ** 2 + (row['y'] - centroid_y) ** 2) ** 0.5
        if distance_to_centroid <= radius:
            points_within_radius[i] += 1

# Plot the points, the centroid, and the circles using x and y coordinates
plt.figure(figsize=(8, 8))
#plt.scatter(data['x'], data['y'], marker='o', color='b', label='Points')
plt.scatter(data['x'], data['y'], marker='o', color=['red' if d <= 2 else 'blue' for d in data.apply(lambda row: ((row['x'] - centroid_x) ** 2 + (row['y'] - centroid_y) ** 2) ** 0.5, axis=1)], label='Points')
plt.scatter(centroid_x, centroid_y, marker='x', color='r', label='Centroid')

# Draw circles for each radius
for radius in radii:
    circle = plt.Circle((centroid_x, centroid_y), radius, fill=False, color='g', linestyle='--', alpha=0.5, label=f'{radius} km Radius')
    plt.gca().add_patch(circle)

plt.xlabel('X Coordinate (km)')
plt.ylabel('Y Coordinate (km)')
plt.title('Points, Centroid, and Circles on the XY Plane')
plt.legend()
plt.grid(True)

# Display the number of points within each radius
for i, radius in enumerate(radii):
    print(f'Number of points within {radius} km radius: {points_within_radius[i]}')

plt.show()