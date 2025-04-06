import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time

from scipy.stats import beta

def show():
    st.markdown("<h1 style='font-size: 36px; font-weight: bold; margin-top: 0; padding-top: 0;'> MAB Simulation Dashboard</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("---")
        metric = st.selectbox("지표 선택", ["CTR", "CVR", "Revenue", "ROAS", "CPA"])

    if metric == "CTR":
        ctr_dict = {'Control': 0.05, 'Test': 0.1}
    elif metric == "CVR":
        ctr_dict = {'Control': 0.07, 'Test': 0.12}
    elif metric == "Revenue":
        ctr_dict = {'Control': 20 / 1000, 'Test': 30 / 1000}
    elif metric == "ROAS":
        ctr_dict = {'Control': 2.5 / 1000, 'Test': 4.0 / 1000}

    arms = ['Control', 'Test']
    epsilon = 0.1

    eg_rewards = []
    ts_rewards = []

    eg_counts = {arm: 0 for arm in arms}
    eg_values = {arm: 0 for arm in arms}

    ts_successes = {arm: 1 for arm in arms}
    ts_failures = {arm: 1 for arm in arms}

    n_rounds = st.number_input("Round", min_value=100, max_value=10000, value=100, step=100)
    run_sim = st.button("▶️ Run Simulation")

    for t in range(n_rounds):
        if random.random() < epsilon:
            eg_arm = random.choice(arms)
        else:
            eg_arm = max(arms, key=lambda arm: eg_values[arm])

        reward = np.random.binomial(1, ctr_dict[eg_arm])
        eg_counts[eg_arm] += 1
        eg_values[eg_arm] += (reward - eg_values[eg_arm]) / eg_counts[eg_arm]
        eg_rewards.append(reward)

        ts_samples = {arm: np.random.beta(ts_successes[arm], ts_failures[arm]) for arm in arms}
        ts_arm = max(ts_samples, key=ts_samples.get)

        reward = np.random.binomial(1, ctr_dict[ts_arm])
        ts_successes[ts_arm] += reward
        ts_failures[ts_arm] += 1 - reward
        ts_rewards.append(reward)

    ab_rewards = []
    for t in range(n_rounds):
        arm = arms[t % 2]
        reward = np.random.binomial(1, ctr_dict[arm])
        ab_rewards.append(reward)

    if run_sim:
        st.markdown(f"<h3 style='font-size: 20px; font-weight: 600; margin-top: 0;'>🕹️ Epsilon-Greedy vs Thompson Sampling ({metric})</h3>", unsafe_allow_html=True)
        placeholder1 = st.empty()
        st.markdown(f"<h3 style='font-size: 20px; font-weight: 600; margin-top: 20px;'>🧪 A/B Test vs Thompson Sampling ({metric})</h3>", unsafe_allow_html=True)
        placeholder2 = st.empty()
        for i in range(50, len(eg_rewards), 50):
            fig1, ax1 = plt.subplots(figsize=(8, 3))
            ax1.plot(np.cumsum(eg_rewards[:i]), label='Epsilon-Greedy', linewidth=2, color="#A0C4FF")
            ax1.plot(np.cumsum(ts_rewards[:i]), label='Thompson Sampling', linewidth=2, color="#FFADAD")
            ax1.set_title(f'Cumulative Reward ({metric})', fontsize=7, fontweight='normal')
            ax1.set_xlabel('')
            ax1.set_ylabel("")
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['left'].set_color("#DDD")
            ax1.spines['bottom'].set_color("#DDD")
            ax1.tick_params(axis='x', colors='#888')
            ax1.tick_params(axis='y', colors='#888')
            ax1.grid(True, linestyle='--', linewidth=0.5, color='#DDD')
            ax1.legend()

            fig2, ax2 = plt.subplots(figsize=(8, 3))
            ax2.plot(np.cumsum(ab_rewards[:i]), label='A/B Test', linewidth=2, color="#A0C4FF")
            ax2.plot(np.cumsum(ts_rewards[:i]), label='Thompson Sampling', linewidth=2, color="#FFADAD")
            ax2.set_title(f'Cumulative Reward Comparison ({metric})', fontsize=7, fontweight='normal')
            ax2.set_xlabel('')
            ax2.set_ylabel("")
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['left'].set_color("#DDD")
            ax2.spines['bottom'].set_color("#DDD")
            ax2.tick_params(axis='x', colors='#888')
            ax2.tick_params(axis='y', colors='#888')
            ax2.grid(True, linestyle='--', linewidth=0.5, color='#DDD')
            ax2.legend()

            placeholder1.pyplot(fig1)
            placeholder2.pyplot(fig2)
            time.sleep(0.001)
