import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import ( QMainWindow, QWidget,
                              QTabWidget, QGridLayout, QLabel,
                              QVBoxLayout, QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer
from data_loader import engine1, sensors

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sensor Monitoring Dashboard')
        self.setFixedSize(1200, 800)

        self.current_cycle = 10  # 시작 사이클
        self.max_cycle = len(engine1)

        # 탭 구성
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 탭1: 그래프 + (토글 버튼 + 일시정지/재생 버튼)
        self.tab1_widget = QWidget()
        tab1_layout = QVBoxLayout()

        self.fig, self.axes = plt.subplots(2, 2, figsize=(11, 6))
        self.canvas = FigureCanvas(self.fig)

        self.is_sliding = True  # 기본값 : 슬라이딩 모드
        self.toggle_btn = QPushButton('전체 보기')
        self.toggle_btn.setStyleSheet('font-size: 14px; padding: 8px;')
        self.toggle_btn.clicked.connect(self.toggle_view)

        self.pause_btn = QPushButton('일시정지')
        self.pause_btn.setStyleSheet('font-size: 14px; padding: 8px;')
        self.pause_btn.clicked.connect(self.toggle_pause)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.toggle_btn)
        btn_layout.addWidget(self.pause_btn)

        tab1_layout.addWidget(self.canvas)
        tab1_layout.addLayout(btn_layout)
        self.tab1_widget.setLayout(tab1_layout)
        self.tabs.addTab(self.tab1_widget, '실시간 모니터링')

        # 탭2: 상태 패널
        self.status_widget = QWidget()
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(50, 50, 50, 50)
        self.status_widget.setLayout(self.grid)
        self.tabs.addTab(self.status_widget, '설비 상태')

        # 상태 패널 헤더
        for col, text in enumerate(['센서', '상태', '현재값']):
            header = QLabel(text)
            header.setAlignment(Qt.AlignCenter)
            header.setStyleSheet('font-size: 16px; font-weight: bold;')
            self.grid.addWidget(header, 0, col)

        # 상태 레이블 저장
        self.status_labels = {}
        self.value_labels = {}
        for i, sensor in enumerate(sensors):
            name_label = QLabel(sensor)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet('font-size: 14px;')

            status_label = QLabel('정상')
            status_label.setAlignment(Qt.AlignCenter)
            status_label.setStyleSheet('font-size: 14px; padding: 10px; border-radius: 5px;')

            value_label = QLabel('-')
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setStyleSheet('font-size: 14px;')

            self.grid.addWidget(name_label, i + 1, 0)
            self.grid.addWidget(status_label, i + 1, 1)
            self.grid.addWidget(value_label, i + 1, 2)

            self.status_labels[sensor] = status_label
            self.value_labels[sensor] = value_label

        # 타이머 설정 (1000ms마다 업데이트)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def get_status(self, sensor, current_data):
        latest = current_data[sensor].iloc[-1]
        mean = engine1[sensor].mean()
        std = engine1[sensor].std()
        if abs(latest - mean) > 2 * std:
            return '위험', 'background-color: red; color: white;'
        elif abs(latest - mean) > std:
            return '주의', 'background-color: yellow;'
        else:
            return '정상', 'background-color: green; color: white;'
        
    def toggle_view(self):
        self.is_sliding = not self.is_sliding
        if self.is_sliding:
            self.toggle_btn.setText('전체 보기')
        else:
            self.toggle_btn.setText('슬라이딩 보기')
        # 일시정지 상태일 때도 즉시 그래프 업데이트
        if not self.timer.isActive():
            self.redraw_graph()

    def redraw_graph(self):
        current_data = engine1.iloc[:self.current_cycle]
        window_size = 30
        window_data = current_data.iloc[-window_size:]

        for ax, sensor in zip(self.axes.flatten(), sensors):
            ax.clear()
            ax.plot(current_data['cycle'], current_data[sensor],
                    color='lightblue', linewidth=1, alpha=0.5)
            ax.plot(window_data['cycle'], window_data[sensor],
                    color='blue', linewidth=1.5)
            ax.scatter(current_data['cycle'].iloc[-1],
                    current_data[sensor].iloc[-1],
                    color='red', s=50, zorder=5)

            if self.is_sliding:
                ax.set_xlim(window_data['cycle'].iloc[0],
                            window_data['cycle'].iloc[-1] + 5)

            ax.set_title(sensor)
            ax.set_xlabel('Cycle')
            ax.set_ylabel('Value')

        self.fig.tight_layout()
        self.canvas.draw()

    def toggle_pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_btn.setText('재생')
        else:
            self.timer.start(1000)
            self.pause_btn.setText('일시정지')

    def update(self):
        if self.current_cycle >= self.max_cycle:
            self.timer.stop()
            return

        self.current_cycle += 1
        current_data= engine1.iloc[:self.current_cycle]

        self.redraw_graph()

        for sensor in sensors:
            status, style = self.get_status(sensor, current_data)
            latest = round(current_data[sensor].iloc[-1], 4)
            self.status_labels[sensor].setStyleSheet(
                style + ' font-size: 14px; padding: 10px; border-radius: 5px;')
            self.status_labels[sensor].setText(status)
            self.value_labels[sensor].setText(str(latest))