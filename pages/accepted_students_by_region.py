import streamlit as st
import pandas as pd

# 로그인 과정 없이 바로 해당 페이지에 들어왔을 때는 ID를 "None"으로 저장함
if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

with st.sidebar:
    # 상위 페이지 ID 정보를 하위 페이지에서 불러옴
    ID = st.session_state["ID"] 
    st.caption(f'{ID}님 접속중')

data = pd.read_csv("c:/Users/admin/OneDrive/바탕 화면/python/basic program/week10/results.csv", encoding='utf-8')
data["졸업년도"] = data["졸업년도"].astype(str)

# 연도 선택 박스 추가
year_options = sorted(data["졸업년도"].unique())
year_options.insert(0, "전체")  # "전체" 옵션 추가
selected_year = st.selectbox("연도를 선택하세요", options=year_options)

# 특정 연도 데이터 필터링
if selected_year == "전체":
    filtered_data = data
else:
    filtered_data = data[data["졸업년도"] == selected_year]

# 내신 구간 옵션 설정
grade_intervals = [
    "1.0-1.5", "1.5-2.0", "2.0-2.5", "2.5-3.0", 
    "3.0-3.5", "3.5-4.0", "4.0-4.5", "4.5-5.0", 
    "5.0-5.5", "5.5-6.0", "6.0-6.5", "6.5-7.0", 
    "7.0-7.5", "7.5-8.0", "8.0-8.5", "8.5-9.0"
]

# 각 구간별 데이터 건수 계산
valid_intervals = []
for interval in grade_intervals:
    min_grade, max_grade = map(float, interval.split('-'))
    count = len(filtered_data[(filtered_data["내신"] >= min_grade) & (filtered_data["내신"] < max_grade)])
    if count > 0:
        valid_intervals.append(interval)

# 유효한 내신 구간으로 라디오 버튼 구성 및 처리
if valid_intervals:
    selected_interval = st.radio("내신 구간을 선택하세요", valid_intervals, horizontal=True)

# 선택된 구간을 최소값과 최대값으로 변환
min_grade, max_grade = map(float, selected_interval.split('-'))

# 선택된 연도와 내신 점수 범위로 데이터 필터링
if selected_year == "전체":
    filtered_data = data[
        (data["내신"] >= min_grade) &
        (data["내신"] < max_grade)
    ]
else:
    filtered_data = data[
        (data["졸업년도"] == selected_year) &
        (data["내신"] >= min_grade) &
        (data["내신"] < max_grade)
    ]

# 각 지역별 데이터 건수 세기 : 새로운 표(df)를 만들고 이름을 location_counts로 지음, 속성으로 [지역/위도/경도/Count] 생성
df = pd.DataFrame(filtered_data)
location_counts = df.groupby(['지역', '위도', '경도', '군']).size().reset_index(name='Count')

# 각 지역의 데이터 크기를 size로 동그라미 크기 표현하고 속성에 [size] 추가 
location_counts['size'] = location_counts['Count'] * 3000  # 크기 조정

color = {'수시':'#37eb9180',
         '정시':'#ebbb3780'}
location_counts.loc[:,'color'] = location_counts.copy().loc[:,'군'].map(color)

# 지도 위에 범례 추가
st.markdown("""
    <style>
    .legend-container {
        display: flex;
        justify-content: center;  /* 가운데 정렬 */
        align-items: center;
        margin-bottom: 20px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        margin-right: 15px; /* 아이템 간 간격 */
    }
    .color-box {
        width: 15px;
        height: 15px;
        margin-right: 5px;
        border: 1px solid black;
    }
    </style>
    <div class="legend-container">
        <div class="legend-item">
            <div class="color-box" style="background-color: #37eb9180;"></div>
            <span>수시 합격생</span>
        </div>
        <div class="legend-item">
            <div class="color-box" style="background-color: #ebbb3780;"></div>
            <span>정시 합격생</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 지도에 데이터 표시
st.map(location_counts,
       latitude="위도",
       longitude="경도",
       size = 'size',
       color = 'color',
       zoom=6)


