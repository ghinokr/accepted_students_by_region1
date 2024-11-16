import streamlit as st
import pandas as pd
import time

# 타이틀을 가운데 정렬 & streamlit에서 HTML 코드 활성화
st.markdown("<h1 style='text-align: center;'>합격자 지역별 비율</h1>", unsafe_allow_html=True)

# 이미지 가운데 정렬
col1, col2, col3 = st.columns([1, 2, 1])  # 가운데 정렬을 위한 컬럼 비율 설정
with col2:
    st.image('accepted_students_by_region.png', width=350)

data = pd.read_csv('members.csv')
# PW를 문자열로 인식!!! 
data["PW"] = data["PW"].astype(str)

st.write("ID\u2003:\u2003홍길동\u2003PW\u2003:\u20031234")

# Streamlit에서 with 구문은 특정 컨텍스트 내에서만 코드 블록이 실행되도록 만드는 방식
# with 구문을 사용하면 코드가 특정 컬럼이나 탭 안에 배치되어 해당 영역에만 적용됩니다.
with st.form("login_form"):
    ID = st.text_input("ID", placeholder="아이디를 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    #form에는 반드시 제출 버튼이 있어야 함
    submit_button = st.form_submit_button("로그인")

if submit_button:
    if not ID or not PW:
        st.warning("ID와 비밀번호를 모두 입력해주세요.")
    else:
        # 사용자 확인 : 입력한 ID와 PW가 회원명부의 데이터와 일치하면 user에 ID와 PW값을 입력
        user = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        
        if not user.empty:
            st.success(f"{ID}님 환영합니다!")
            # 하위 페이지에서도 ID 정보를 그대로 사용하기 위함
            st.session_state["ID"]=ID
            
            progress_text = "로그인 중입니다."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            st.switch_page('pages/accepted_students_by_region.py')
            
            
        else:
            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
