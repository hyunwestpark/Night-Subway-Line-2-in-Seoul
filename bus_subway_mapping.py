import pandas as pd
from geopy.distance import geodesic

# 파일 경로
bus_csv_path = "./merged_bus_data.csv"
subway_csv_path = "./subway_number2_data.csv"

# 데이터 불러오기
def load_data(bus_path, subway_path):
    bus_df = pd.read_csv(bus_path)
    subway_df = pd.read_csv(subway_path, encoding="cp949")
    return bus_df, subway_df

# 가까운 지하철 역 매핑
def match_nearest_subway(bus_df, subway_df):
    matched_data = []
    for _, bus in bus_df.iterrows():
        try:
            # 위도와 경도 순서 확인
            bus_coords = (bus["Y좌표"], bus["X좌표"])
            nearest_station = None
            min_distance = float("inf")
            for _, subway in subway_df.iterrows():
                subway_coords = (subway["위도"], subway["경도"])
                distance = geodesic(bus_coords, subway_coords).meters
                if distance < min_distance:
                    min_distance = distance
                    nearest_station = subway["역명"]
            matched_data.append({
                **bus,
                "매칭된지하철역": nearest_station,
                "역과거리(m)": min_distance,
            })
        except ValueError as e:
            print(f"Invalid coordinates: Bus {bus_coords}, Subway {subway_coords}. Error: {e}")
            continue
    return pd.DataFrame(matched_data)

# 4. CSV 파일 저장
def save_to_csv(dataframe, output_path):
    dataframe.to_csv(output_path, index=False)
    print(f"CSV 파일이 저장되었습니다: {output_path}")


# 5. 실행
def main():
    # 데이터 로드
    bus_df, subway_df = load_data(bus_csv_path, subway_csv_path)

    # 매칭 수행
    matched_df = match_nearest_subway(bus_df, subway_df)

    # 결과 저장
    output_path = "matched_bus_to_subway.csv"
    save_to_csv(matched_df, output_path)


if __name__ == "__main__":
    main()