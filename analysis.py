import glob
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def get_paths():
    paths = []
    for filename in glob.glob("logs/*"):
        with open(filename, 'r') as f:
            paths.append([])
            reader = csv.reader(f, delimiter=",")
            for i, line in enumerate(reader):
                paths[-1].append(line)
    return paths

def show_paths():
    paths = get_paths()
    colors = cm.rainbow(np.linspace(0, 1, len(paths)))
    for path, c in zip(paths, colors):
        x = []
        y = []
        for point in path:
            x.append(eval(point[0])[0])
            y.append(eval(point[0])[1])
        plt.plot(x, y, color=c)
    plt.show()

def show_heatmap():
    paths = get_paths()
    x = []
    y = []
    for path in paths:
        for point in path:
            x.append(eval(point[0])[0])
            y.append(eval(point[0])[1])
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=(20, 20))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
 
    # Plot heatmap
    plt.clf()
    plt.title('Room Heatmap')
    plt.ylabel('y')
    plt.xlabel('x')
    plt.imshow(heatmap, extent=extent, origin="lower")
    plt.show()