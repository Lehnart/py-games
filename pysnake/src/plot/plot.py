import time
import os
import json
import matplotlib.pyplot as plt
import numpy as np

plt.ion()
plt.show()
fig, axes = plt.subplots(2,2,figsize=(16,10))
while True :

    filenames = []
    for r, d, files in os.walk(os.getcwd() + "/results"):
        for filename in files:
            if '.txt' in filename:
                filenames.append(os.path.join(r, filename))

    durations = []
    move_counts = []
    apple_eat_counts = []
    for filename in filenames:
        with open(filename,"r") as f :
            data = json.load(f)
            durations.append( data["t_end"] - data["t_start"] )
            move_counts.append( data["move_count"] )
            apple_eat_counts.append(data["apple_eat_count"])

    means = []
    medians = []
    percentiles_75 = []
    percentiles_90 = []
    percentiles_99 = []

    for last_index in range(1,len(durations)) :
        means.append( np.mean(apple_eat_counts[:last_index] ) )
        medians.append(np.percentile(apple_eat_counts[:last_index], 50))
        percentiles_75.append(np.percentile(apple_eat_counts[:last_index], 75))
        percentiles_90.append(np.percentile(apple_eat_counts[:last_index], 90))
        percentiles_99.append(np.percentile(apple_eat_counts[:last_index], 99))

    axes[0][0].clear()
    axes[0][0].hist(apple_eat_counts,bins=[i+0.5 for i in range(50)])
    axes[0][0].set_title("Apple eat distribution")

    axes[0][1].clear()
    axes[0][1].hist(move_counts,bins=100)
    axes[0][1].set_title("Move count distribution")

    axes[1][0].clear()
    axes[1][0].scatter(durations, apple_eat_counts)
    axes[1][0].set_title("Apple eat vs time")

    axes[1][1].clear()
    axes[1][1].plot(means, label="mean")
    axes[1][1].plot(medians, label="median")
    # axes[1][1].plot(percentiles_75, label="75 percentile")
    # axes[1][1].plot(percentiles_90, label="90 percentile")
    # axes[1][1].plot(percentiles_99, label="99 percentile")
    axes[1][1].legend()
    axes[1][1].set_title("Quantiles of apple count, mean = " + str(means[-1]))

    plt.draw()
    plt.pause(1.)

    time.sleep(30)


