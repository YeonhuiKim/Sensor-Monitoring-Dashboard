import pandas as pd
import matplotlib.pyplot as plt

dir_path = "./CMAPSSData/";

columns = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + \
        [f'sensor_{i}' for i in range(1, 22)]


df = pd.read_csv(dir_path + 'train_FD001.txt', sep=r'\s+', header=None, names=columns);


engine1=df[df['engine_id'] == 1];


fig, axes = plt.subplots(2, 2, figsize=(12, 8))

sensors = ['sensor_2', 'sensor_7', 'sensor_14', 'sensor_20']

for ax, sensor in zip(axes.flatten(), sensors):
    ax.plot(engine1['cycle'], engine1[sensor])
    ax.set_title(sensor)
    ax.set_xlabel('Cycle')
    ax.set_ylabel('Value')

plt.tight_layout()
plt.show()