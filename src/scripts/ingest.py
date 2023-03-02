import os
import glob
import time
from datetime import datetime
from tqdm import tqdm
from django.db import IntegrityError, transaction
from app.models import WeatherRecord


def run():
    # Define the path to the directory containing the weather data files
    data_dir = '../wx_data/'

    # Get a list of all the weather data files in the directory
    data_files = glob.glob(os.path.join(data_dir, '*.txt'))

    # Keep track of the number of records ingested
    num_records = 0

    # Keep track of the start time
    start_time = time.time()

    # Loop over each data file
    for data_file in tqdm(data_files):
        # Extract the station ID from the file name
        station_id = os.path.splitext(os.path.basename(data_file))[0]

        # Open the file and loop over each line
        with open(data_file, 'r') as f:
            for line in f:
                # Split the line into fields
                fields = line.strip().split('\t')

                # Parse the fields
                date = datetime.strptime(fields[0], '%Y%m%d').date()
                max_temp = float(fields[1]) / 10 if fields[1] != '-9999' else None
                min_temp = float(fields[2]) / 10 if fields[2] != '-9999' else None
                precipitation = float(fields[3]) / \
                    10 if fields[3] != '-9999' else None

                # Create a new WeatherRecord object
                record = WeatherRecord(date=date, max_temp=max_temp, min_temp=min_temp,
                                    precipitation=precipitation, station_id=station_id)

                # Attempt to save the record to the database
                try:
                    with transaction.atomic():
                        record.save()
                        num_records += 1
                except IntegrityError:
                    # If a record with the same date and station ID already exists, skip this record
                    pass

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time

    # Print a summary of the results
    print(f"Ingested {num_records} records in {elapsed_time:.2f} seconds")
