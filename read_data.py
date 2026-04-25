import pandas as pd

dir_path = "./CMAPSSData/";

columns = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + \
        [f'sensor_{i}' for i in range(1, 20)]

df = pd.read_csv(dir_path + 'train_FD001.txt', sep='\\s+', header=None, names=columns);

print(df.head());
print(df.shape);