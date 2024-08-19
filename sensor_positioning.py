import math
import numpy as np
import json

# Function to find the peak intensity value and its corresponding distance
def find_peak(data):
    peak_index = np.argmax(data['y'])
    peak_distance = data['x'][peak_index]
    return peak_distance

# Function to convert polar coordinates to Cartesian coordinates
def convert_to_coordinates(distance, angle, radius):
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x + distance * math.cos(angle), y + distance * math.sin(angle)

# Function to estimate the position of the object
def estimate_position(sensor_data, radius=600, min_intensity_threshold=50):
    coordinates = []
    angles = [0, 2 * math.pi / 3, 4 * math.pi / 3]  # 0°, 120°, 240° in radians

    for i, data in enumerate(sensor_data):
        peak_index = np.argmax(data['y'])
        peak_intensity = data['y'][peak_index]
        peak_distance = data['x'][peak_index]
        
        # If peak intensity is below the threshold, assume no object
        if peak_intensity < min_intensity_threshold:
            print(f"Sensor {data['a']} detects low intensity. Object might be absent.")
            return None, None
        
        x, y = convert_to_coordinates(peak_distance, angles[i], radius)
        coordinates.append((x, y))

    # Calculate the average position
    avg_x = sum([coord[0] for coord in coordinates]) / len(coordinates)
    avg_y = sum([coord[1] for coord in coordinates]) / len(coordinates)

    return avg_x, avg_y

# Function to check if the object is within the detection circle
def is_object_present(estimated_position, radius=600):
    if estimated_position[0] is None or estimated_position[1] is None:
        return False
    
    distance_from_center = math.sqrt(estimated_position[0]**2 + estimated_position[1]**2)
    return distance_from_center <= radius

# Load sensor data from JSON files
def load_sensor_data(filenames):
    sensor_data = []
    for filename in filenames:
        with open(filename, 'r') as f:
            data = json.load(f)
            sensor_data.append(data)
    return sensor_data

# Main function
def main():
    # List of JSON files containing sensor data
    sensor_files = ['sensor1.json', 'sensor2.json', 'sensor3.json']
    sensor_data = load_sensor_data(sensor_files)

    # Estimate the position of the object
    estimated_position = estimate_position(sensor_data)
    
    if estimated_position[0] is None and estimated_position[1] is None:
        print("Object might be absent.")
    else:
        print("Estimated Position:", estimated_position)

        # Check if the object is within the circle
        if is_object_present(estimated_position):
            print("Object is present within the circle.")
        else:
            print("Object is not present within the circle.")

if __name__ == "__main__":
    main()
