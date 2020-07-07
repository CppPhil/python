import matplotlib.pyplot as plt
import csv
import sys

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

            # Read gyroscope data if there's some, otherwise just use 0.0.
            hasGyroscopeIndexThreshold = 7

            if len(row) > hasGyroscopeIndexThreshold:
                gyroscopeX.append(float(row[gyroscopeXColumnIndex]))
                gyroscopeY.append(float(row[gyroscopeYColumnIndex]))
                gyroscopeZ.append(float(row[gyroscopeZColumnIndex]))
            else:
                gyroscopeX.append(0.0)
                gyroscopeY.append(0.0)
                gyroscopeZ.append(0.0)

    plt.plot(time, hardwareTimestamp, extractId, accelerometerX, accelerometerY, accelerometerZ, gyroscopeX, gyroscopeY,
             gyroscopeZ, marker='o')

    plt.title(csv_file_path)

    plt.show()
