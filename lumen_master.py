import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. 페이지 기본 설정 및 새로운 타이틀 적용
st.set_page_config(page_title="루멘 퀀트 스포츠 분석", page_icon="⚽", layout="wide")

st.title("⚽ 루멘 퀀트 스포츠 분석 시뮬레이션 엔진")
st.markdown("---")
st.write("배트맨 승부식 축구 경기 실시간 데이터 기반 몬테카를로 예측 시스템")

# 2. 사이드바 - 시뮬레이션 및 크롤링 설정
st.sidebar.header("⚙️ 시스템 통제소")
sim_count = st.sidebar.number_input(
    "시뮬레이션 반복 횟수 설정", 
    min_value=1000, 
    max_value=5000000, 
    value=500000, 
    step=50000
)
st.sidebar.write(f"현재 가동 준비된 평행우주: **{sim_count:,} 번**")

# 3. 데이터 수집(Crawling) 제어부 신설
st.subheader("📡 실시간 데이터 파이프라인")
col_crawl, col_upload = st.columns(2)

with col_crawl:
    st.info("배트맨 승부식 회차별 축구 대상 경기 데이터를 수집합니다.")
    if st.button("🌐 배트맨 승부식 데이터 크롤링 가동"):
        # 추후 Selenium 크롤러 코드가 이식될 자리입니다.
        with st.spinner("대상 경기 및 배당률 데이터를 추출하고 있습니다... (보안 우회 중)"):
            time.sleep(3) # 크롤링 대기 시간 시뮬레이션
            st.success("데이터 크롤링 임무 완료! (현재는 UI 시연 모드입니다)")
            
with col_upload:
    st.info("크롤링이 막힐 경우를 대비한 수동 엑셀 파일 업로드 기능입니다.")
    uploaded_file = st.file_uploader("승부식 축구 데이터 엑셀 업로드", type=['csv', 'xlsx'])

# 4. 실전 경기 분석 엔진 (임시 더미 데이터로 크롤링 결과 대체)
st.markdown("---")
st.subheader("🎯 축구 승무패 정밀 타겟팅 분석")

# 크롤링으로 수집될 데이터의 형태를 미리 정의합니다.
crawled_data = pd.DataFrame({
    '경기번호': [101, 102, 103],
    '리그': ['EPL', 'LaLiga', 'Serie A'],
    '홈팀': ['아스널', '레알 마드리드', '인터밀란'],
    '원정팀': ['첼시', '바르셀로나', 'AC밀란'],
    '홈_xG(예상)': [1.8, 1.5, 1.2],
    '원정_xG(예상)': [1.1, 1.6, 1.0]
})

st.dataframe(crawled_data, use_container_width=True)

selected_match = st.selectbox(
    "몬테카를로 난수를 적용할 축구 경기를 선택하십시오:", 
    crawled_data['홈팀'] + " vs " + crawled_data['원정팀']
)

# 5. 핵심 엔진: 푸아송 분포 난수 생성 및 결과 도출
if st.button("🚀 선택 경기 500만 번 평행우주 시뮬레이션"):
    with st.spinner(f"초고속 연산 중... {sim_count:,} 번의 가상 경기를 진행하고 있습니다."):
        
        # 선택된 경기의 인덱스를 찾아 xG 값을 매칭합니다.
        match_idx = crawled_data[crawled_data['홈팀'] + " vs " + crawled_data['원정팀'] == selected_match].index[0]
        home_xg = crawled_data.loc[match_idx, '홈_xG(예상)']
        away_xg = crawled_data.loc[match_idx, '원정_xG(예상)']
        
        # 푸아송 난수 매트릭스 생성
        home_goals_sim = np.random.poisson(home_xg, sim_count)
        away_goals_sim = np.random.poisson(away_xg, sim_count)
        
        # 승무패 통계 추출
        home_wins = np.sum(home_goals_sim > away_goals_sim)
        draws = np.sum(home_goals_sim == away_goals_sim)
        away_wins = np.sum(home_goals_sim < away_goals_sim)
        
        prob_home = (home_wins / sim_count) * 100
        prob_draw = (draws / sim_count) * 100
        prob_away = (away_wins / sim_count) * 100
        
        # 결과 대시보드 출력
        col1, col2, col3 = st.columns(3)
        col1.metric("🏠 홈팀 승리 확률", f"{prob_home:.2f}%")
        col2.metric("🤝 무승부 확률", f"{prob_draw:.2f}%")
        col3.metric("✈️ 원정팀 승리 확률", f"{prob_away:.2f}%")
        
        result_df = pd.DataFrame({
            '경기 결과': ['홈팀 승리', '무승부', '원정팀 승리'],
            '확률 (%)': [prob_home, prob_draw, prob_away]
        })
        
        st.bar_chart(result_df.set_index('경기 결과'))
