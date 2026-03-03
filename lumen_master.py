import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 기본 설정
st.set_page_config(page_title="루멘 축구승무패 퀀트", page_icon="⚽", layout="wide")

# 2. 메인 타이틀 및 UI
st.title("⚽ 루멘 퀀트: 축구승무패 몬테카를로 시뮬레이션 엔진")
st.markdown("---")
st.write("축구승무패 분석의 새로운 지평을 여는 평행우주 시뮬레이션 엔진에 오신 것을 환영합니다.")

# 3. 사이드바 - 시뮬레이션 설정 (미니콘다 환경 최적화)
st.sidebar.header("⚙️ 시뮬레이션 세팅")
sim_count = st.sidebar.number_input(
    "시뮬레이션 반복 횟수 설정", 
    min_value=1000, 
    max_value=5000000, 
    value=500000, 
    step=50000
)
st.sidebar.write(f"현재 가동 준비된 평행우주: **{sim_count:,} 번**")

# 4. 분석 데이터 (홈/원정 팀의 기대 득점 - xG)
# 향후 엑셀 데이터 연동을 위한 초석입니다.
matches_data = {
    '아스널 vs 맨체스터 시티': {'Home_xG': 1.2, 'Away_xG': 1.6},
    '리버풀 vs 첼시': {'Home_xG': 1.8, 'Away_xG': 1.1},
    '토트넘 vs 맨체스터 유나이티드': {'Home_xG': 1.5, 'Away_xG': 1.4},
    '레알 마드리드 vs 바르셀로나': {'Home_xG': 1.7, 'Away_xG': 1.5}
}

selected_match = st.selectbox("정밀 분석을 진행할 축구 경기를 선택하십시오:", list(matches_data.keys()))

# 5. 핵심 엔진: 푸아송 분포를 활용한 축구승무패 예측
if st.button("🚀 축구승무패 몬테카를로 분석 가동"):
    with st.spinner(f"초고속 연산 중... {sim_count:,} 번의 가상 경기를 진행하고 있습니다."):
        
        home_xg = matches_data[selected_match]['Home_xG']
        away_xg = matches_data[selected_match]['Away_xG']
        
        # 푸아송 분포 난수를 이용한 홈/원정팀 득점 시뮬레이션 생성
        home_goals_sim = np.random.poisson(home_xg, sim_count)
        away_goals_sim = np.random.poisson(away_xg, sim_count)
        
        # 승/무/패 조건 매트릭스 도출
        home_wins = np.sum(home_goals_sim > away_goals_sim)
        draws = np.sum(home_goals_sim == away_goals_sim)
        away_wins = np.sum(home_goals_sim < away_goals_sim)
        
        # 최종 백분율(%) 확률 계산
        prob_home = (home_wins / sim_count) * 100
        prob_draw = (draws / sim_count) * 100
        prob_away = (away_wins / sim_count) * 100
        
        st.success("데이터 시뮬레이션 분석이 완벽하게 완료되었습니다!")
        
        # 6. 대시보드 핵심 지표 출력
        col1, col2, col3 = st.columns(3)
        col1.metric("🏠 홈팀 승리 확률", f"{prob_home:.2f}%")
        col2.metric("🤝 무승부 확률", f"{prob_draw:.2f}%")
        col3.metric("✈️ 원정팀 승리 확률", f"{prob_away:.2f}%")
        
        # 7. 시각화 (서버 충돌 및 폰트 깨짐이 없는 스트림릿 내장 차트 사용)
        result_df = pd.DataFrame({
            '경기 결과': ['홈팀 승리', '무승부', '원정팀 승리'],
            '확률 (%)': [prob_home, prob_draw, prob_away]
        })
        
        st.subheader("📊 축구승무패 예측 데이터 시각화")
        st.bar_chart(result_df.set_index('경기 결과'))
        
        st.info("💡 본 시스템은 축구 경기의 특성인 '푸아송 분포'를 기반으로, 각 팀의 기대 득점(xG)을 활용해 대규모 몬테카를로 평행우주를 생성하여 가장 합리적인 승무패 통계를 도출합니다.")
