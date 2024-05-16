import json
import random
import datetime

data = []

# Generate 10 temperature recordings
for i in range(100):
    # Generate a random temperature between 15 and 30
    temperature = random.uniform(15, 30)
    # Round the temperature to 2 digits
    temperature = round(temperature, 2)
    
    # Generate a timestamp 5 minutes apart
    timestamp = (datetime.datetime.now() + datetime.timedelta(minutes=i*5)).strftime("%H:%M")
    
    # Create a dictionary for the temperature recording
    recording = {
        "timestamp": timestamp,
        "temperature": temperature
    }
    
    # Add the recording to the data list
    data.append(recording)

# Write the data to a JSON file
with open("temperatures.json", "w") as file:
    json.dump(data, file)