# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import constants as c
import csv
import numpy as np


def parse_bot_logs():
    with open('data.csv', mode='w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(["heuristic", "look_ahead", "trials", "moves", "highest_tile", "score"])
        log_files = list(c.LOG_FILES.values())
        for file in log_files:
            print(file)
            heuristic = file[file.index("_") + 1:file.index(".")]
            print(heuristic)
            with open(file, mode='r') as g:
                lines = g.readlines()

            data = {"look_ahead": [], "trials": [], "moves": [], "highest_tile": [], "score": []}
            for line in lines:
                # print(line)
                line = line.strip()
                # print(line)
                row = [heuristic]
                stats = line.split(" ")
                for stat in stats:
                    name, value = stat.split(":")
                    row.append(int(value))
                    data[name].append(value)
                writer.writerow(row)
                row = []

        """look_ahead:1 trials:1 moves:72 highest_tile:32 score:440"""


def parse_bot_logs_by_look_ahead(trials):
    all_data = {}
    log_files = list(c.LOG_FILES.values())
    for file in log_files:
        print(file)
        heuristic = file[file.index("_") + 1:file.index(".")]
        all_data[heuristic] = {}
        with open(file, mode='r') as g:
            lines = g.readlines()

        # data = {"look_ahead": [], "trials": [], "moves": [], "highest_tile": [], "score": []}
        data = {}  # {1: {}, 2: {}, 3: {}, 4: {}}
        for line in lines:
            line = line.strip()
            stats = line.split(" ")
            for i in range(len(stats)):
                stats[i] = stats[i].split(":")
            # only specific number of trials
            if int(stats[1][1]) == trials:
                look_ahead = int(stats[0][1])
                if look_ahead not in list(data.keys()):
                    data[look_ahead] = {"moves": [], "highest_tile": [], "score": []}
                for i in range(2, 5):
                    data[look_ahead][stats[i][0]].append(int(stats[i][1]))
        # print(data)

        with open("logs/log_summary.txt", mode='a') as f:
            f.write(heuristic + '\n')

        for l in list(data.keys()):
            with open("logs/log_summary.txt", mode='a') as f:
                f.write("\tlook_ahead:{}\n".format(l))

            for stat in list(data[l].keys()):
                results = np.asarray(data[l][stat])
                mean = round(np.mean(results), 2)
                max = round(np.amax(results), 2)
                if stat == 'highest_tile':
                    prop_won = round(len(results[results >= 2048]) / len(results) * 100, 2)
                data[l][stat] = mean

                with open("logs/log_summary.txt", mode='a') as f:
                    f.write("\t\t" + stat.ljust(15))
                    f.write("mean:{}".format(mean).ljust(15))
                    f.write("max:{}".format(max).ljust(15))
                    if stat == 'highest_tile':
                        f.write("prop_won:{}".format(prop_won).ljust(15))
                    f.write("\n")

        all_data[heuristic] = data
        print(data)

    print(all_data)
    return all_data


def parse_bot_logs_by_trials(look_ahead):
    all_data = {}
    log_files = list(c.LOG_FILES.values())
    for file in log_files:
        heuristic = file[file.index("_") + 1:file.index(".")]
        all_data[heuristic] = {}
        with open(file, mode='r') as g:
            lines = g.readlines()

        # data = {"look_ahead": [], "trials": [], "moves": [], "highest_tile": [], "score": []}
        data = {}  # {1: {}, 2: {}, 3: {}, 4: {}}
        for line in lines:
            line = line.strip()
            stats = line.split(" ")
            for i in range(len(stats)):
                stats[i] = stats[i].split(":")
            # only specific number of trials
            if int(stats[0][1]) == look_ahead or heuristic == 'random':
                trials = int(stats[1][1])
                if trials not in list(data.keys()):
                    data[trials] = {"moves": [], "highest_tile": [], "score": []}
                for i in range(2, 5):
                    data[trials][stats[i][0]].append(int(stats[i][1]))

        # print(data)

        with open("logs/log_summary.txt", mode='a') as f:
            f.write(heuristic + '\n')

        for t in list(data.keys()):
            with open("logs/log_summary.txt", mode='a') as f:
                f.write("\ttrials:{}\n".format(t))

            for stat in list(data[t].keys()):
                results = np.asarray(data[t][stat])
                mean = round(np.mean(results), 2)
                max = round(np.amax(results), 2)
                if stat == 'highest_tile':
                    prop_won = round(len(results[results >= 2048]) / len(results) * 100, 2)
                data[t][stat] = mean

                with open("logs/log_summary.txt", mode='a') as f:
                    f.write("\t\t" + stat.ljust(15))
                    f.write("mean:{}".format(mean).ljust(15))
                    f.write("max:{}".format(max).ljust(15))
                    if stat == 'highest_tile':
                        f.write("prop_won:{}".format(prop_won).ljust(15))
                    f.write("\n")

        all_data[heuristic] = data
        print(data)

    print(all_data)
    return all_data


def single_plot(x_data, y_data, title, x_label, y_label):
    """
    Function to make a single plot.
    :param x_data: (list) The x-values.
    :param y_data: (list) The y-values corresponding to the x-values.
    :param title: (str) The title of the plot.
    :param x_label: (str) The x-axis label.
    :param y_label: (str) The y-axis label.
    :return: None
    """
    plt.figure(1, (18, 8))  # something, plot size
    plt.subplot(111)
    plt.plot(x_data, y_data)
    plt.title(title)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    # plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()


def multi_line_plot(x_data, y_data, title, x_label, y_label, line_labels):
    """
    Function to plot multiple lines on the same plot.
    :param x_data: (list of lists) Each list corresponds to a set of x-values to plot.
    :param y_data: (list of lists) Each list corresponds to the corresponding set of y-values to plot.
    :param title: (str) The title of the plot.
    :param x_label: (str) The x-axis label.
    :param y_label: (str) The y-axis label.
    :return: None
    """
    plt.figure(1, (18, 8))  # something, plot size
    plt.subplot(111)
    legend = []
    for i in range(len(x_data)):
        plt.plot(x_data[i], y_data[i], label="yah")
        legend.append(line_labels[i])
    plt.title(title)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.legend(legend, loc='upper left')
    plt.show()


def multi_plot(plot_1, plot_2, *args):
    plot_list = [plot_1, plot_2]
    for plot in args:
        plot_list.append(plot)
    plt.figure(1, (18, 8))

    n = len(plot_list)
    for i in range(n):
        id = '1' + str(n) + str(i)  # 1 plot of n plots, in position i
        plot_list[i].subplt(int(id))

    plt.show()


def make_subplot(x_data, y_data, title, x_label, y_label):
    plt.plot(x_data, y_data)
    plt.title(title)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)


if __name__ == "__main__":
    open("logs/log_summary.txt", 'w').close()

    # parse_bot_logs()
    ''' change? '''
    data = parse_bot_logs_by_look_ahead(trials=1)
    for x in [2, 3, 4, 5]:
        data['random'][x] = data['random'][1]

    x = [list(data[heuristic].keys()) for heuristic in data.keys()]
    print(x)

    y_axis = "score"
    y = []
    for heuristic in data.keys():
        y.append([data[heuristic][l][y_axis] for l in data[heuristic].keys()])
    print(y)
    multi_line_plot(x_data=x, y_data=y, title="", x_label="look ahead", y_label=y_axis, line_labels=list(data.keys()))

    '''change to 4? '''
    data = parse_bot_logs_by_trials(look_ahead=3)
    for x in [2, 4, 6, 8, 10]:
        data['random'][x] = data['random'][1]

    x = [list(data[heuristic].keys()) for heuristic in data.keys()]
    print(x)
    y = []
    for heuristic in data.keys():
        y.append([data[heuristic][l][y_axis] for l in data[heuristic].keys()])
    print(y)
    multi_line_plot(x_data=x, y_data=y, title="", x_label="trials", y_label=y_axis,
                    line_labels=list(data.keys()))
