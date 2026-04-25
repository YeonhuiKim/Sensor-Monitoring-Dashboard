import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QVBoxLayout, QTabWidget, QGridLayout, QLabel)
from PyQt5.QtCore import Qt

dir_path = "./CMAPSSData/";

columns = ['engine_id', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + \
        [f'sensor_{i}' for i in range(1, 23)]


df = pd.read_csv(dir_path + 'train_FD001.txt', sep=r'\s+', header=None, names=columns);
engine1=df[df['engine_id'] == 1];

# 센서 선택 기준: max-min 값이 큰 센서(변화가 있어 모니터링의 의미가 있는 센서)
sensors = ['sensor_2', 'sensor_7', 'sensor_14', 'sensor_20']

# 탭1: 센서 데이터 그래프
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, sensor in zip(axes.flatten(), sensors):
    ax.plot(engine1['cycle'], engine1[sensor])
    ax.set_title(sensor)
    ax.set_xlabel('Cycle')
    ax.set_ylabel('Value')
plt.tight_layout()
canvas = FigureCanvas(fig)

# 탭2: 상태 패널
def get_status(sensor):
    latest = engine1[sensor].iloc[-1]
    mean = engine1[sensor].mean()
    std = engine1[sensor].std()
    # 위험: 평균에서 2표준편차 이상 벗어남
    # 주의: 평균에서 1표준편차 이상 벗어남
    # 정상: 평균에서 1표준편차 이내
    if abs(latest - mean) > 2 * std:
        return '위험', 'background-color: red; color: white;'
    elif abs(latest - mean) > std:
        return '주의', 'background-color: yellow;'
    else:
        return '정상', 'background-color: green; color: white;'
    
status_widget = QWidget()
grid = QGridLayout()

for i, sensor in enumerate(sensors):
    status, style = get_status(sensor)
    label_name = QLabel(sensor)
    label_name.setAlignment(Qt.AlignCenter)
    label_status = QLabel(status)
    label_status.setAlignment(Qt.AlignCenter)
    label_status.setStyleSheet(style + ' font-size: 20px; padding: 20px;')
    grid.addWidget(label_name, i, 0)
    grid.addWidget(label_status, i, 1)

status_widget.setLayout(grid)


# 메인 윈도우
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('Sensor Monitoring Dashboard')
window.setFixedSize(1200, 800)

tabs = QTabWidget()
tabs.addTab(canvas, '실시간 모니터링')
tabs.addTab(status_widget, '설비 상태')
window.setCentralWidget(tabs)

window.show()
sys.exit(app.exec_())