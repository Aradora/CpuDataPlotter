import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sys
import csv

filename = ''
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print('Add <file>.csv as argument. Exiting.')
    exit(2)

with open(filename,'r') as f_input:
    csv_input = csv.reader(filter(lambda inRow: inRow[0] != '#', f_input), delimiter=',')
    labels = next(csv_input)
    data = [[] for i in range(len(labels))]
    lineNumber = 0
    try:
        for row in csv_input:
            lineNumber = lineNumber + 1
            for index, dane in enumerate(row):
                if index == 0:
                    data[index].append(datetime.datetime.strptime(dane, "%H:%M:%S"))
                else:
                    data[index].append(int(dane))

    except:
        print("ERR: Bad data format at line: " + str(lineNumber))
        print(row)
        print('Exiting.')
        exit(1)

    data[0] = [data[0][0] + datetime.timedelta(seconds=i) for i in range(len(data[0]))]
    #magic number comes from experiments
    width = int(len(data[0]) / 29)
    length = 4

    if width * 100 > pow(2,16):
        width = int(pow(2,16))
        print('Reached max width for plot: ' + str(width) + ' pixels')

    fig, ax = plt.subplots(figsize=(width, length))

    ax.grid(True)

    plt.MaxNLocator(5)

    for i in range(len(data)-1):
        ax.plot(data[0],data[i+1],label = labels[i+1])

    start, end = ax.get_xlim()
#   formatting x axis marking
    hours = mdates.HourLocator(interval=1)
    h_fmt = mdates.DateFormatter('%H:%M:%S')

#   formatting density of x axis markings
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    ax.xaxis.set_ticks(np.arange(start, end, 0.00035))
    ax.tick_params(axis='x', rotation=45)

    plt.ylabel('%-value')
    plt.title('KULTURA PRACY CPU')
    plt.xlabel(labels[0])
    plt.legend()

    filename = filename.replace('.csv', '.png')
    plt.savefig(filename, bbox_inches='tight')
    print('Done.')
    exit(0)
