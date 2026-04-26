# Sensor Monitoring Dashboard

NASA CMAPSS 데이터셋을 활용한 설비 센서 실시간 모니터링 대시보드입니다.
Python과 PyQt5로 구현했습니다.

## 주요 기능
- 센서 데이터 실시간 시각화(1초마다 갱신)
- 슬라이딩 윈도우(최근 30개 데이터) / 전체 보기 토글
- 일시정지 / 재생
- 설비 상태 패널(정상/주의/위험)

## 사용 데이터
NASA CMAPSS(Commercial Modular Aero-Propulsion System Simulation) 데이터셋을 사용합니다.

CMAPSS 데이터셋은 터보팬 엔진의 센서 데이터를 시뮬레이션한 공개 데이터셋으로, 설비 예측 보전 연구에 널리 활용되고 있습니다.
- NASA CMAPSS 데이터셋 다운로드: https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

## 모니터링 센서 선택 기준
전체 21개 센서 중, 변화량(max-min)이 큰 센서를 선택했습니다.

그 중 시간의 흐름에 따라 추세가 나타나는 2, 7, 14, 20번의 4개 센서를 선택했습니다.

## 설비 상태 판단 기준
현재 사이클의 센서값이 전체 평균에서 얼마나 벗어났는지를 기준으로 판단했습니다.
| 상태 | 기준 |
|------|------|
| 정상 | 평균에서 1 표준편차 이내 |
| 주의 | 평균에서 1 ~ 2 표준편차 벗어남 |
| 위험 | 평균에서 2 표준편차 이상 벗어남 |

## 실행 방법
1. 패키지 설치

   pip install pandas matplotlib PyQt5
2. NASA CMAPSS 데이터 다운로드 후 'CMAPSSData' 폴더에 저장
3. 실행

   python main.py

## 사용 기술
- Python
- PyQt5
- matplotlib
- pandas
