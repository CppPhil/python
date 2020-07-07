import matplotlib.pyplot as plt
import csv
import sys
import pandas as pd

if __name__ == "__main__":
    argc = len(sys.argv)
    expectedArgumentCount = 2

    if argc != expectedArgumentCount:
        print(f"Too few command line arguments provided: {argc - 1}, expected {expectedArgumentCount - 1}")
        exit(-1)

    csv_file_path_index = 1
    csv_file_path = sys.argv[csv_file_path_index]

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

    # plt.plot(time, hardwareTimestamp, extractId, accelerometerX, accelerometerY, accelerometerZ, gyroscopeX,
    # gyroscopeY, gyroscopeZ, marker='o')

    # plt.plot(hardwareTimestamp, extractId, accelerometerX, marker='o')

    rightArmSensorId = 769
    bellySensorId = 770
    chestSensorId = 771
    leftArmSensorId = 772

    #  df = pd.DataFrame({''})

    # map than maps HWTimestamp to
    #      maps that (each) map extractId to the 6 channels.

    data = {}

    for i in range(len(time)):
        currentHardwareTimestamp = hardwareTimestamp[i]
        sensorId = extractId[i]
        channel1 = accelerometerX[i]
        channel2 = accelerometerY[i]
        channel3 = accelerometerZ[i]
        channel4 = gyroscopeX[i]
        channel5 = gyroscopeY[i]
        channel6 = gyroscopeZ[i]

        channelList = [channel1, channel2, channel3, channel4, channel5, channel6]

        timestampMap = data.get(currentHardwareTimestamp)

        if timestampMap is None:
            data[currentHardwareTimestamp] = {sensorId: channelList}
        else:
            timestampMap[sensorId] = channelList
            data[currentHardwareTimestamp] = timestampMap

    # TODO: FUBAR'D FUBAR'D FUBAR'D FUBAR'D FUBAR'D FUBAR'D
    # TODO: Hardware timestamp is not unique as it wraps around.

    # Have time axis <-
    #           sensor 1: If there's a channel1 value for the time: SHOW IT
    #           sensor 2: If there's a channel1 value for the time: SHOW IT
    #           sensor 3: If there's a channel1 value for the time: SHOW IT
    #           sensor 4: If there's a channel1 value for the time: SHOW IT

    # List of the time
    # sensor1list: has REAL entry if there's something, otherwise previous entry

    uniqueHardwareTimestamps = list(dict.fromkeys(hardwareTimestamp))
    channel1RightArmSensor = []
    channel1BellySensor = []
    channel1ChestSensor = []
    channel1LeftArmSensor = []

    for timestamp in uniqueHardwareTimestamps:
        timestampMap = data.get(timestamp)
        channel1RightArmSensor.append(timestampMap.get(rightArmSensorId)[0])
        channel1BellySensor.append(timestampMap.get(bellySensorId)[0])
        channel1ChestSensor.append(timestampMap.get(bellySensorId)[0])
        channel1LeftArmSensor.append(timestampMap.get(leftArmSensorId)[0])

    df = pd.DataFrame({'hardware_timestamp': uniqueHardwareTimestamps, 'channel1_right_arm': channel1RightArmSensor,
                       'channel1_belly': channel1BellySensor, 'channel1_chest': channel1ChestSensor,
                       'channel1_left_arm': channel1LeftArmSensor})

    plt.plot('hardware_timestamp', 'channel1_right_arm', data=df, marker='o', markerfacecolor='blue', color='skyblue')
    plt.plot('hardware_timestamp', 'channel1_belly', data=df, marker='', color='olive')
    plt.plot('hardware_timestamp', 'channel1_chest', data=df, marker='', color='red', linestyle='dashed')
    plt.plot('hardware_timestamp', 'channel1_left_arm', data=df, marker='x', color='orange')

    plt.title(csv_file_path)
    plt.ylabel('time')
    plt.xlabel('measurement')

    plt.show()
