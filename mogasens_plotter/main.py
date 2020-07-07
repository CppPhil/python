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


def sensor_to_string(sensorId):
    right_arm_sensor_id = 769
    belly_sensor_id = 770
    chest_sensor_id = 771
    left_arm_sensor_id = 772

    if sensorId == right_arm_sensor_id:
        return "right arm sensor"
    elif sensorId == belly_sensor_id:
        return "belly sensor"
    elif sensorId == chest_sensor_id:
        return "chest sensor"
    elif sensorId == left_arm_sensor_id:
        return "left arm sensor"
    else:
        return f"bogus sensor, id: {sensorId}"


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

    timeColumnIndex = 0
    hardwareTimestampColumnIndex = 1
    extractIdColumnIndex = 2
    # We don't care about the trigger (it's always 0).
    accelerometerXColumnIndex = 4
    accelerometerYColumnIndex = 5
    accelerometerZColumnIndex = 6
    gyroscopeXColumnIndex = 7
    gyroscopeYColumnIndex = 8
    gyroscopeZColumnIndex = 9

    time = []
    hardwareTimestamp = []
    extractId = []
    accelerometerX = []
    accelerometerY = []
    accelerometerZ = []
    gyroscopeX = []
    gyroscopeY = []
    gyroscopeZ = []

    with open(csv_file_path, 'r') as csv_file:
        plots = csv.reader(csv_file, delimiter=',')
        for rowCount, row in enumerate(plots):
            if rowCount == 0:  # Skip the header row
                continue

            time.append(float(row[timeColumnIndex]))
            hardwareTimestamp.append(int(row[hardwareTimestampColumnIndex]))
            extractId.append(int(row[extractIdColumnIndex]))
            accelerometerX.append(float(row[accelerometerXColumnIndex]))
            accelerometerY.append(float(row[accelerometerYColumnIndex]))
            accelerometerZ.append(float(row[accelerometerZColumnIndex]))
            gyroscopeX.append(float(row[gyroscopeXColumnIndex]))
            gyroscopeY.append(float(row[gyroscopeYColumnIndex]))
            gyroscopeZ.append(float(row[gyroscopeZColumnIndex]))

    timeData = []
    channelData = []

    for i in range(len(time)):
        currentSensorId = extractId[i]

        if currentSensorId == desired_sensor:
            timeData.append(time[i])

            if desired_channel == 1:
                channelData.append(accelerometerX[i])
            elif desired_channel == 2:
                channelData.append(accelerometerY[i])
            elif desired_channel == 3:
                channelData.append(accelerometerZ[i])
            elif desired_channel == 4:
                channelData.append(gyroscopeX[i])
            elif desired_channel == 5:
                channelData.append(gyroscopeY[i])
            elif desired_channel == 6:
                channelData.append(gyroscopeZ[i])

    df = pd.DataFrame({'time': timeData, 'channel': channelData})

    plt.plot('time', 'channel', data=df, color='skyblue')
    plt.title(csv_file_path)
    plt.ylabel(f'{channel_to_string(desired_channel)} {sensor_to_string(desired_sensor)}')
    plt.xlabel('time')
    plt.show()
