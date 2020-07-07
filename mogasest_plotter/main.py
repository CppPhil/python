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

    # Have time axis <-
    #           sensor 1: If there's a channel1 value for the time: SHOW IT
    #           sensor 2: If there's a channel1 value for the time: SHOW IT
    #           sensor 3: If there's a channel1 value for the time: SHOW IT
    #           sensor 4: If there's a channel1 value for the time: SHOW IT

    # List of the time
    # sensor1list: has REAL entry if there's something, otherwise previous entry

    channel1RightArmSensor = []
    channel1BellySensor = []
    channel1ChestSensor = []
    channel1LeftArmSensor = []

    for i in range(len(time)):
        currentSensorId = extractId[i]

        if currentSensorId == rightArmSensorId:
            channel1RightArmSensor.append(accelerometerX[i])
            append_previous(channel1BellySensor, i)
            append_previous(channel1ChestSensor, i)
            append_previous(channel1LeftArmSensor, i)
        elif currentSensorId == bellySensorId:
            append_previous(channel1RightArmSensor, i)
            channel1BellySensor.append(accelerometerX[i])
            append_previous(channel1ChestSensor, i)
            append_previous(channel1LeftArmSensor, i)
        elif currentSensorId == chestSensorId:
            append_previous(channel1RightArmSensor, i)
            append_previous(channel1BellySensor, i)
            channel1ChestSensor.append(accelerometerX[i])
            append_previous(channel1LeftArmSensor, i)
        elif currentSensorId == leftArmSensorId:
            append_previous(channel1RightArmSensor, i)
            append_previous(channel1BellySensor, i)
            append_previous(channel1ChestSensor, i)
            channel1LeftArmSensor.append(accelerometerX[i])

    df = pd.DataFrame({'time': time, 'channel1_right_arm': channel1RightArmSensor,
                       'channel1_belly': channel1BellySensor, 'channel1_chest': channel1ChestSensor,
                       'channel1_left_arm': channel1LeftArmSensor})

    plt.plot('time', 'channel1_right_arm', data=df, color='skyblue')
    # plt.plot('time', 'channel1_belly', data=df, color='olive')
    # plt.plot('time', 'channel1_chest', data=df, color='red')
    # plt.plot('time', 'channel1_left_arm', data=df, color='orange')

    plt.title(csv_file_path)
    plt.ylabel('channel1 right arm')
    plt.xlabel('time')

    plt.show()
