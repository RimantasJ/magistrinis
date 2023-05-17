import numpy as np
import pandas as pd
import csv
from global_variables import *

# Converting txt file to csv
def txt_to_csv(file_path):
    read_file = pd.read_csv(file_path)
    csv_file_path = file_path[:-3] + 'csv'
    read_file.to_csv(csv_file_path, index=None)
    return csv_file_path


def csv_to_array(csv_file_path):
    csv_file = open(csv_file_path)
    csvreader = csv.reader(csv_file)
    next(csvreader)
    ts, dr = [], []
    for row in csvreader:
        ts.append(row[1])
        dr.append(row[2:])

    timestamps = np.array(ts, dtype=int)
    dosimeter_values = np.array(dr, dtype=float)

    return timestamps, dosimeter_values

def array_to_csv(file_name, header, timestamps, real_coordinates, calculated_coordinates):
    res_file = open((file_name + '.csv'), 'w')
    write = csv.writer(res_file) 
    write.writerow(header) 
    for t, r, c in zip(timestamps, real_coordinates, calculated_coordinates):
        write.writerow([t,r,c]) 

def clear_radiation_noise(ds_values, threshold):
    for row in ds_values:
        for i, value in enumerate(row):
            if (value < threshold):
                row[i] = 0

def get_real_coordinates(
    timestamps,
    radiation_data,
    start_coordinate=START_COORDINATE,
    start_time=TIMER_START_OFFSET,
    step_time=STEP_TIME,
    step_size=STEP_SIZE,
    cutoff_margin=STEP_CUTOFF_MARGIN,
    going_down=IS_GOING_DOWN,
):
    def get_step_timestamp(step_num):
        return start_time + step_num * step_time
    
    def get_step_coordinate(step_num):
        return start_coordinate + step_num * step_size * (1 if going_down else -1)

    def is_timestamp_in_cutoff(ts):
        return (
            (ts > get_step_timestamp(curr_step_num) and ts < get_step_timestamp(curr_step_num) + cutoff_margin) or
            (ts > get_step_timestamp(curr_step_num+1) - cutoff_margin and ts < get_step_timestamp(curr_step_num+1))
        )
        
    real_coordinates = np.zeros(len(timestamps))
    curr_step_num = 0
    i = np.argmax(radiation_data[0] > 0.02)
    start_time = timestamps[i]

    for i, timestamp in enumerate(timestamps):
        if timestamp > get_step_timestamp(curr_step_num+1):
            curr_step_num += 1
        
        if not is_timestamp_in_cutoff(int(timestamp)):
            real_coordinates[i] = get_step_coordinate(curr_step_num)
        
    return real_coordinates