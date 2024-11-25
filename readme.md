# 서울 지하철 2호선 심야 운행 분석

이 프로젝트는 Simio 시뮬레이션 소프트웨어에서 사용할 데이터를 준비하기 위해 설계되었습니다. 주요 목표는 서울 지하철 2호선을 심야 시간에 운행할 때 어떤 역이 적합한지 분석하는 것입니다. 버스 및 지하철 승객 데이터를 처리하고 집계하여 Simio 입력에 적합한 CSV 파일을 생성합니다.

## 준비 사항
이 프로젝트를 실행하려면 다음 라이브러리 설치가 필요합니다:

- 데이터 조작을 위한 **Pandas** (`pip install pandas`)
- 지리적 거리 계산을 위해 **Geopy**  (`pip install geopy`)

## 파일 구조
- `bus_data_preprocessing.py`
  - **이용 데이터**
    - `bus_data.csv` (서울시 버스노선별 정류장별 시간대별 승하차 인원 정보 데이터 파일입니다.)
    - 출처: [서울시 열린 데이터 광장](https://data.seoul.go.kr/dataList/OA-12913/S/1/datasetView.do)
  - **기능**: `bus_data.csv`에서 불필요한 컬럼을 제거하고 N버스와 00시부터 05시까지의 운행 정보를 남기는 스크립트입니다.
  - **산출물**: `preprocessed_bus_data.csv`

- `merge_bus_coordinates.py`
  - **이용 데이터**
    - `preprocessed_bus_data.csv`
    - `bus_stop_data.csv`
      - 출처: [서울시 열린 데이터 광장](https://data.seoul.go.kr/dataList/OA-15067/S/1/datasetView.do)
  - **기능**: 버스 정류장 데이터에 좌표를 할당하여 데이터를 병합합니다.
  - **산출물**: `merged_bus_data.csv`

- `bus_subway_mapping.py`
  - **이용 데이터**
    - `merged_bus_data.csv`
    - `subway_number2_data.csv`
      - 출처: [공공 데이터 포털](https://www.data.go.kr/data/15041301/fileData.do)
  - **기능**: 각 버스 정류장에서 가장 가까운 지하철역을 `geopy`를 사용하여 매핑하는 작업을 수행합니다.
  - **산출물**: `matched_bus_to_subway.csv`

- `simio_data_preparation.py`
  - **이용 데이터**: `matched_bus_to_subway.csv`
  - **기능**: Simio에서 사용할 데이터를 처리하고 준비하는 메인 스크립트입니다.
  - **산출물**: `simio_station_demand.csv`