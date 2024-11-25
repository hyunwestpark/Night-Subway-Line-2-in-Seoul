import pandas as pd

# 파일 경로 설정
matched_csv_path = "./matched_bus_to_subway.csv"


# 데이터 불러오기
def load_matched_data(csv_path):
    return pd.read_csv(csv_path)


# 심야 시간대 승차 및 하차 인원 계산
def calculate_night_passengers(bus_df):
    # 각 시간대별 승차 및 하차 인원 계산 (00시부터 5시까지)
    night_hours = ['00시', '1시', '2시', '3시', '4시', '5시']
    for hour in night_hours:
        bus_df[f'{hour}_심야_승차'] = bus_df[f'{hour}승차총승객수']
        bus_df[f'{hour}_심야_하차'] = bus_df[f'{hour}하차총승객수']
    return bus_df


# 역 단위로 이용 승객 추정치 집계
def aggregate_station_demand(bus_df):
    night_hours = ['00시', '1시', '2시', '3시', '4시', '5시']
    agg_dict = {}
    for hour in night_hours:
        agg_dict[f'{hour}_심야_승차'] = 'sum'
        agg_dict[f'{hour}_심야_하차'] = 'sum'
    station_demand = bus_df.groupby('매칭된지하철역').agg(agg_dict).reset_index()

    # 각 시간대별 탑승 추정치 계산 (승차와 하차의 평균)
    # 승차와 하차를 더한 후 나눈 이유는 역에 대한 수요를 의미하기 떄문임
    for hour in night_hours:
        station_demand[f'{hour}_심야_탑승_추정'] = (station_demand[f'{hour}_심야_승차'] + station_demand[f'{hour}_심야_하차']) / 2

    columns_to_keep = ['매칭된지하철역'] + [f'{hour}_심야_탑승_추정' for hour in night_hours]
    station_demand = station_demand[columns_to_keep]

    return station_demand


# CSV 파일 저장
def save_to_csv(dataframe, output_path):
    dataframe.to_csv(output_path, index=False)
    print(f"CSV 파일이 저장되었습니다: {output_path}")


# 실행
def main():
    # 데이터 로드
    matched_df = load_matched_data(matched_csv_path)

    # 심야 시간대 승차 및 하차 인원 계산
    matched_df = calculate_night_passengers(matched_df)

    # 역 단위 수요 집계
    station_demand = aggregate_station_demand(matched_df)

    # 결과 저장
    output_path = "simio_station_demand.csv"
    save_to_csv(station_demand, output_path)


if __name__ == "__main__":
    main()