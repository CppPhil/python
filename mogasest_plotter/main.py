import matplotlib.pyplot as plt
import csv
import sys
import pandas as pd


def append_previous(the_list, index):
    if len(the_list) >= index > 0:
        the_list.append(the_list[index - 1])
    else:
        the_list.append(0)


if __name__ == "__main__":
    argc = len(sys.argv)
    expectedArgumentCount = 2

    if argc != expectedArgumentCount:
        print(f"Too few command line arguments provided: {argc - 1}, expected {expectedArgumentCount - 1}")
        exit(-1)

    csv_file_path_index = 1
    csv_file_path = sys.argv[csv_file_path_index]

    # TODO: Read these from the command line somehow
    desired_sensor = 769
    desired_channel = 1

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

    rightArmSensorId = 769
    bellySensorId = 770
    chestSensorId = 771
    leftArmSensorId = 772

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
    plt.ylabel(f'channel{desired_channel} {desired_sensor}')  # TODO: Make the printing of this prettier
    plt.xlabel('time')
    plt.show()
