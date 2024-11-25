import pandas as pd

# 데이터 불러오기
bus_data = pd.read_csv("bus_data.csv", encoding = "cp949")

# 노선번호가 'N'으로 시작하는 데이터만 필터링
filtered_data = bus_data[bus_data['노선번호'].str.startswith('N')]

# 심야 시간대만 남기기
filtered_columns = [col for col in filtered_data.columns if col[:2]  in ["00", "1시", "2시", "3시", "4시", "5시"]]

# 주요 열
filtered_data = filtered_data[["표준버스정류장ID", "노선번호", "역명"] + filtered_columns]

# 정류장명 중복 제거
unique_data = filtered_data.drop_duplicates(subset='역명')

# 결과 저장
unique_data.to_csv("preprocessed_bus_data.csv", index=False)

# 결과 확인
print(unique_data)
