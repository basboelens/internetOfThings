import re
import os
from datetime import datetime
import time

file_path = "data.txt" 
file_size = os.path.getsize(file_path)

def extract_data():
    values = []
    timer = 0
    info = []

    # Read data from data.txt
    with open(file_path, "r") as file:
        lines = file.readlines()[-100:]
        for line in lines:
            line = line.split()
            for data in line:
                # Get the correct data values
                if data.startswith('"1-0:1.7.0'):
                    if timer >= 10:
                        print("na timer 60------------")
                        print(sum(info))
                        print(len(info))
                        average = [sum(info) / len(info)]
                        timer = 0
                        print("avg hieronder")
                        print(average)
                        return average
                    else:
                        # Select only the data value
                        data = data.split('(')[1].split(')')[0]
                        value = re.sub('[\D]', "", data)
                        # Add to list to return
                        info.append(int(value))
                        timer += 1
                        print("hieronder")
                        print(info)
                        print(data)
                        time.sleep(2)
    file.close()
