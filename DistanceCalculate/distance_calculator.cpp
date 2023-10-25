#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <string>
#include <sstream>
#include <stdexcept>
#include <limits> 
#include <iomanip> 

using namespace std;

const double EarthRadiusKm = 6371.0;

struct Coordinate {
    double latitude;
    double longitude;

    // Constructor to initialize the Coordinate struct
    Coordinate(double lat, double lon) : latitude(lat), longitude(lon) {}
};

double DegreesToRadians(double degrees) {
    return degrees * M_PI / 180.0;
}

double CalculateDistance(const Coordinate& coord1, const Coordinate& coord2) {
    double dLat = DegreesToRadians(coord2.latitude - coord1.latitude);
    double dLon = DegreesToRadians(coord2.longitude - coord1.longitude);

    double a = sin(dLat / 2) * sin(dLat / 2) + cos(DegreesToRadians(coord1.latitude)) * cos(DegreesToRadians(coord2.latitude)) * sin(dLon / 2) * sin(dLon / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));

    return EarthRadiusKm * c;
}

int main() {
    ifstream inputFile("/Users/moctran/Desktop/HUST/LabDrone/Multi-objective_truck_drone/TestGenerator/GetCoordinates/results.csv");
    if (!inputFile.is_open()) {
        cerr << "Failed to open input file." << endl;
        return 1;
    }

    // Create a vector to store coordinates
    vector<Coordinate> coordinates;

    // Read and parse the CSV file
    string line;
    int lineNum = 0; // To keep track of the line number
    while (getline(inputFile, line)) {
        lineNum++; // Increment line number

        // Skip the first line (header)
        if (lineNum == 1) {
            continue;
        }

        stringstream ss(line);
        string latitudeStr, longitudeStr;
        getline(ss, latitudeStr, ',');
        getline(ss, longitudeStr, ',');

        try {
            double latitude = stod(latitudeStr);
            double longitude = stod(longitudeStr);
            coordinates.push_back(Coordinate(latitude, longitude)); // Construct Coordinate objects
        } catch (const std::invalid_argument& e) {
            cerr << "Error parsing latitude or longitude on line " << lineNum << ": " << e.what() << endl;
        }
    }

    inputFile.close();

    // Calculate the distance matrix
    int numPoints = coordinates.size();
    vector<vector<double> > distanceMatrix(numPoints, vector<double>(numPoints, 0.0)); // Note the space in '> >'

    for (int i = 0; i < numPoints; ++i) {
        for (int j = 0; j < numPoints; ++j) {
            if (i != j) {
                distanceMatrix[i][j] = CalculateDistance(coordinates[i], coordinates[j]);
            }
        }
    }

    // Calculate longest, shortest, and average distances
    double longestDistance = -1.0; // Initialize to a negative value
    double shortestDistance = numeric_limits<double>::max(); // Initialize to the maximum possible value
    double totalDistance = 0.0;

    for (int i = 0; i < numPoints; ++i) {
        for (int j = 0; j < numPoints; ++j) {
            if (i != j) {
                double distance = distanceMatrix[i][j];
                totalDistance += distance;

                if (distance > longestDistance) {
                    longestDistance = distance;
                }
                if (distance < shortestDistance) {
                    cout << i << " " << j << endl;
                    shortestDistance = distance;
                }
            }
        }
    }

    double averageDistance = totalDistance / (numPoints * (numPoints - 1));

    // Open the output text file
    ofstream outputFile("distance_matrix.txt");
    if (!outputFile.is_open()) {
        cerr << "Failed to open output file." << endl;
        return 1;
    }
    outputFile << "distance (km)" << endl;
    // Write the distance matrix to the text file
    for (int i = 0; i < numPoints; ++i) {
        for (int j = 0; j < numPoints; ++j) {
            outputFile << distanceMatrix[i][j] << " ";
        }
        outputFile << endl;
    }

    // Output longest, shortest, and average distances
    // cout << "Longest Distance: " << longestDistance << " km" << endl;
    // cout << "Shortest Distance: " << shortestDistance << " km" << endl;
    // cout << "Average Distance: " << averageDistance << " km" << endl;

    outputFile << "Longest Distance: " << longestDistance << " km" << endl;
    outputFile << "Shortest Distance: " << shortestDistance << " km" << endl;
    outputFile << "Average Distance: " << averageDistance << " km" << endl;

    outputFile.close();

    return 0;
}
