import requests
import pandas as pd
from datetime import datetime
import os  # This helps us check if the file exists on your computer


def append_data_to_csv():
    url = "http://api.citybik.es/v2/networks/callabike-frankfurt"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        stations = data['network']['stations']

        station_list = []
        for station in stations:
            station_info = {
                'station_name': station['name'],
                'free_bikes': station['free_bikes'],
                'empty_slots': station['empty_slots'],
                'latitude': station['latitude'],
                'longitude': station['longitude'],
                'timestamp': datetime.now()
            }
            station_list.append(station_info)

        df = pd.DataFrame(station_list)

        filename = "frankfurt_bikes.csv"

        # --- THE MAGIC PART IS HERE ---
        # Check if the file already exists
        if os.path.isfile(filename):
            # If it exists, append (add to bottom) without writing the header names again
            df.to_csv(filename, mode='a', header=False, index=False)
            print(f"✅ Added new data to {filename}!")
        else:
            # If it does NOT exist, create it and write the header names
            df.to_csv(filename, mode='w', header=True, index=False)
            print(f"✅ Created new file {filename}!")

    else:
        print("❌ Error fetching data.")


if __name__ == "__main__":
    append_data_to_csv()