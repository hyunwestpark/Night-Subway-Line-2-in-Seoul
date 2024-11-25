import pandas as pd

# 1. 전처리된 N버스 데이터 불러오기
n_bus_data = pd.read_csv("preprocessed_bus_data.csv")

# 2. 버스정류소 위치정보 데이터 불러오기
bus_stop_data = pd.read_csv("bus_stop_data.csv", encoding="cp949")

# 3. 키 확인 및 데이터 전처리 (필요한 열만 선택)
# bus_stop_data에서 필요한 열만 남김
bus_stop_data = bus_stop_data[["노드 ID", "정류소명", "X좌표", "Y좌표"]]

# 4. 조인 수행 (표준버스정류장ID와 노드ID를 키로 사용)
merged_data = pd.merge(
    n_bus_data,
    bus_stop_data,
    left_on="표준버스정류장ID",  # N버스 데이터의 키
    right_on="노드 ID",          # 정류소 위치 데이터의 키
    how="inner"                # 공통 데이터만 남김
)

# 5. 불필요한 열 제거 (예: 조인 후 중복된 키)
merged_data = merged_data.drop(columns=["노드 ID", "역명"])

# 6. 결과 저장
merged_data.to_csv("merged_bus_data.csv", index=False)

# 결과 확인
print(merged_data.head())
