import re
import os

file_path = "C:\\Users\\hado\\Documents\\School\\IoT Project\\internetOfThings\\internetOfThings\\data.txt"

def extract_data():
    values = []
    # Read data from data.txt
    with open(file_path, "r") as file:
        for line in file:
            line = line.split()
            for data in line:
                # Get the correct data values
                if data.startswith('"1-0:1.7.0'):
                    # Select only the data value
                    data = data.split('(')[1].split(')')[0]
                    value = re.sub('[\D]', "", data)
                    # Add to list to return
                    values.append(value)
    file.close()
    return values
