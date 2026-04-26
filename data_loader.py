import pandas as pd

dir_path = "./CMAPSSData/"

columns = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + \
        [f'sensor_{i}' for i in range(1, 23)]

df = pd.read_csv(dir_path + 'train_FD001.txt', sep='\s+', header=None, names=columns)
engine1 = df[df['engine_id'] == 1].reset_index(drop=True)   # 1번 엔진 데이터만 사용, 데이터 인덱스 초기화

# 센서 선택 기준: max-min 값이 큰 센서(변화가 있어 모니터링의 의미가 있는 센서)
sensors = ['sensor_2', 'sensor_7', 'sensor_14', 'sensor_20']