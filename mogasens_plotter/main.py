#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Sensors
# 769 = right arm
# 770 = belly
# 771 = chest
# 772 = left arm

# Channels
# 1 = accelerometer X                                                                                       
# 2 = accelerometer Y                                                                                       
# 3 = accelerometer Z                                                                                       
# 4 = gyroscope X                                                                                           
# 5 = gyroscope Y                                                                                           
# 6 = gyroscope Z   

import argparse
import csv

import matplotlib.pyplot as plt
import pandas as pd


def sensor_to_string(sensor_id):
    right_arm_sensor_id = 769
    belly_sensor_id = 770
    chest_sensor_id = 771
    left_arm_sensor_id = 772

    if sensor_id == right_arm_sensor_id:
        return "right arm sensor"
    elif sensor_id == belly_sensor_id:
        return "belly sensor"
    elif sensor_id == chest_sensor_id:
        return "chest sensor"
    elif sensor_id == left_arm_sensor_id:
        return "left arm sensor"
    else:
        return f"bogus sensor, id: {sensor_id}"


def channel_to_string(channel):
    if channel == 1:
        return "accelerometer X"
    elif channel == 2:
        return "accelerometer Y"
    elif channel == 3:
        return "accelerometer Z"
    elif channel == 4:
        return "gyroscope X"
    elif channel == 5:
        return "gyroscope Y"
    elif channel == 6:
        return "gyroscope Z"
    else:
        return f"bogus channel: {channel}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot MoGaSens CSV file.')
    parser.add_argument('csv_file_path', type=str, help='Path to the CSV file to plot.')
    parser.add_argument('sensor', type=int, help='The sensor to plot.')
    parser.add_argument('channel', type=int, help='The channel to plot.')

    args = parser.parse_args()

    csv_file_path = args.csv_file_path
    desired_sensor = args.sensor
    desired_channel = args.channel

    time_column_index = 0
    # We don't care about the hardware timestamp.
    extract_id_column_index = 2
    # We don't care about the trigger (it's always 0).
    accelerometer_x_column_index = 4
    accelerometer_y_column_index = 5
    accelerometer_z_column_index = 6
    gyroscope_x_column_index = 7
    gyroscope_y_column_index = 8
    gyroscope_z_column_index = 9

    time = []
    extract_id = []
    accelerometer_x = []
    accelerometer_y = []
    accelerometer_z = []
    gyroscope_x = []
    gyroscope_y = []
    gyroscope_z = []

    with open(csv_file_path, 'r') as csv_file:
        plots = csv.reader(csv_file, delimiter=',')
        for row_count, row in enumerate(plots):
            if row_count == 0:  # Skip the header row
                continue

            time.append(float(row[time_column_index]))
            extract_id.append(int(row[extract_id_column_index]))
            accelerometer_x.append(float(row[accelerometer_x_column_index]))
            accelerometer_y.append(float(row[accelerometer_y_column_index]))
            accelerometer_z.append(float(row[accelerometer_z_column_index]))
            gyroscope_x.append(float(row[gyroscope_x_column_index]))
            gyroscope_y.append(float(row[gyroscope_y_column_index]))
            gyroscope_z.append(float(row[gyroscope_z_column_index]))

    time_data = []
    channel_data = []

    for i in range(len(time)):
        current_sensor_id = extract_id[i]

        if current_sensor_id == desired_sensor:
            time_data.append(time[i])

            if desired_channel == 1:
                channel_data.append(accelerometer_x[i])
            elif desired_channel == 2:
                channel_data.append(accelerometer_y[i])
            elif desired_channel == 3:
                channel_data.append(accelerometer_z[i])
            elif desired_channel == 4:
                channel_data.append(gyroscope_x[i])
            elif desired_channel == 5:
                channel_data.append(gyroscope_y[i])
            elif desired_channel == 6:
                channel_data.append(gyroscope_z[i])

    df = pd.DataFrame({'time': time_data, 'channel': channel_data})

    plt.plot('time', 'channel', data=df, color='skyblue')
    plt.title(csv_file_path)
    plt.ylabel(f'{channel_to_string(desired_channel)} {sensor_to_string(desired_sensor)}')
    plt.xlabel('time')
    plt.show()
