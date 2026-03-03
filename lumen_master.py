import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Lumen Soccer Quant", page_icon="⚽", layout="wide")

# 2. Main Title and UI
st.title("⚽ Lumen Quant: Soccer Match Prediction System")
st.markdown("---")
st.write("Welcome to the Monte Carlo Simulation Engine for Soccer Match Analysis.")

# 3. Sidebar - Monte Carlo Parameters
st.sidebar.header("⚙️ Simulation Settings")
sim_count = st.sidebar.number_input("Number of Simulations", min_value=1000, max_value=5000000, value=50000, step=10000)
st.sidebar.write(f"Current Target: **{sim_count:,} parallel universes**")

# 4. Mock Data (Expected Goals - xG for Home and Away teams)
# In the future, this can be replaced with an Excel/CSV upload feature.
matches_data = {
    'Arsenal vs Man City': {'Home_xG': 1.2, 'Away_xG': 1.6},
    'Liverpool vs Chelsea': {'Home_xG': 1.8, 'Away_xG': 1.1},
    'Tottenham vs Man Utd': {'Home_xG': 1.5, 'Away_xG': 1.4},
    'Real Madrid vs Barcelona': {'Home_xG': 1.7, 'Away_xG': 1.5}
}

selected_match = st.selectbox("Select a Match for Analysis:", list(matches_data.keys()))

# 5. Core Engine: Monte Carlo Simulation using Poisson Distribution
if st.button("🚀 Run Monte Carlo Analysis"):
    with st.spinner(f"Running {sim_count:,} simulations... Please wait."):
        
        home_xg = matches_data[selected_match]['Home_xG']
        away_xg = matches_data[selected_match]['Away_xG']
        
        # Simulating match outcomes using numpy's poisson generator
        home_goals_sim = np.random.poisson(home_xg, sim_count)
        away_goals_sim = np.random.poisson(away_xg, sim_count)
        
        # Calculating results matrix
        home_wins = np.sum(home_goals_sim > away_goals_sim)
        draws = np.sum(home_goals_sim == away_goals_sim)
        away_wins = np.sum(home_goals_sim < away_goals_sim)
        
        # Calculating final probabilities
        prob_home = (home_wins / sim_count) * 100
        prob_draw = (draws / sim_count) * 100
        prob_away = (away_wins / sim_count) * 100
        
        st.success("Simulation Complete!")
        
        # 6. Dashboard Metrics Display
        col1, col2, col3 = st.columns(3)
        col1.metric("Home Win Probability", f"{prob_home:.2f}%")
        col2.metric("Draw Probability", f"{prob_draw:.2f}%")
        col3.metric("Away Win Probability", f"{prob_away:.2f}%")
        
        # 7. Visualization (Using Safe Native Streamlit Charts)
        result_df = pd.DataFrame({
            'Outcome': ['Home Win', 'Draw', 'Away Win'],
            'Probability (%)': [prob_home, prob_draw, prob_away]
        })
        
        st.subheader("📊 Match Prediction Chart")
        # Native charts prevent any font-missing crashes on Linux servers
        st.bar_chart(result_df.set_index('Outcome'))
        
        st.info("💡 This analysis utilizes a Poisson distribution-based Monte Carlo method to predict sports outcomes.")
