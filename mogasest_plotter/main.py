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

    plt.title(csv_file_path)
    plt.ylabel('time')
    plt.xlabel('measurement')

    plt.show()
