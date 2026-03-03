import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 기본 설정
st.set_page_config(page_title="루멘 퀀트 스포츠 분석", page_icon="⚽", layout="wide")

st.title("⚽ 루멘 퀀트 스포츠 분석 시뮬레이션 엔진")
st.markdown("---")
st.write("배트맨 승부식 축구 경기 데이터 기반 몬테카를로 예측 시스템")

# 2. 사이드바 - 시뮬레이션 설정
st.sidebar.header("⚙️ 시스템 통제소")
sim_count = st.sidebar.number_input(
    "시뮬레이션 반복 횟수 설정", 
    min_value=1000, 
    max_value=5000000, 
    value=500000, 
    step=50000
)
st.sidebar.write(f"현재 가동 준비된 평행우주: **{sim_count:,} 번**")

# 3. 데이터 업로드 제어부
st.subheader("📁 승부식 축구 데이터 엑셀 연동")
st.info("배트맨 대상 경기와 팀별 예상 득점(xG)이 정리된 엑셀 파일을 업로드해 주십시오.")

# 파일 업로드 버튼 생성 (엑셀, CSV 지원)
uploaded_file = st.file_uploader("여기를 클릭하여 엑셀(.xlsx) 또는 CSV 파일을 올려주세요.", type=['csv', 'xlsx'])

# 4. 실전 경기 분석 엔진
st.markdown("---")
st.subheader("🎯 축구 승무패 정밀 타겟팅 분석")

if uploaded_file is not None:
    # 엑셀 파일이 업로드 되면 판다스로 읽어들임
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.success("배트맨 축구 대상 경기 데이터가 성공적으로 엔진에 주입되었습니다!")
    st.dataframe(df, use_container_width=True)
    
    # 엑셀 데이터의 '홈팀'과 '원정팀' 열을 조합하여 선택 상자 생성
    try:
        selected_match = st.selectbox(
            "정밀 몬테카를로 분석을 진행할 경기를 선택하십시오:", 
            df['홈팀'] + " vs " + df['원정팀']
        )
        
        # 5. 핵심 엔진 가동
        if st.button("🚀 선택 경기 500만 번 평행우주 시뮬레이션 가동"):
            with st.spinner(f"초고속 연산 중... {sim_count:,} 번의 가상 경기를 진행하고 있습니다."):
                
                # 선택한 경기의 xG 데이터 추출
                match_idx = df[df['홈팀'] + " vs " + df['원정팀'] == selected_match].index[0]
                home_xg = float(df.loc[match_idx, '홈_xG'])
                away_xg = float(df.loc[match_idx, '원정_xG'])
                
                # 푸아송 분포 난수 500만 개 동시 생성
                home_goals_sim = np.random.poisson(home_xg, sim_count)
                away_goals_sim = np.random.poisson(away_xg, sim_count)
                
                # 승무패 조건 판별
                home_wins = np.sum(home_goals_sim > away_goals_sim)
                draws = np.sum(home_goals_sim == away_goals_sim)
                away_wins = np.sum(home_goals_sim < away_goals_sim)
                
                # 확률(%) 계산
                prob_home = (home_wins / sim_count) * 100
                prob_draw = (draws / sim_count) * 100
                prob_away = (away_wins / sim_count) * 100
                
                # 결과 출력
                col1, col2, col3 = st.columns(3)
                col1.metric("🏠 홈팀 승리 확률", f"{prob_home:.2f}%")
                col2.metric("🤝 무승부 확률", f"{prob_draw:.2f}%")
                col3.metric("✈️ 원정팀 승리 확률", f"{prob_away:.2f}%")
                
                result_df = pd.DataFrame({
                    '경기 결과': ['홈팀 승리', '무승부', '원정팀 승리'],
                    '확률 (%)': [prob_home, prob_draw, prob_away]
                })
                
                st.bar_chart(result_df.set_index('경기 결과'))
                
    except KeyError:
        st.error("🚨 엑셀 파일의 열(Column) 이름이 잘못되었습니다. 첫 줄에 반드시 '홈팀', '원정팀', '홈_xG', '원정_xG' 라고 정확히 적혀 있어야 합니다.")
        
else:
    st.warning("분석을 시작하려면 먼저 배트맨 데이터 엑셀 파일을 업로드해야 합니다.")
