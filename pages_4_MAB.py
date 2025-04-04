import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

from scipy.stats import beta

def show():
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
    n_rounds = 2000
    epsilon = 0.1

    eg_rewards = []
    ts_rewards = []

    eg_counts = {arm: 0 for arm in arms}
    eg_values = {arm: 0 for arm in arms}

    ts_successes = {arm: 1 for arm in arms}
    ts_failures = {arm: 1 for arm in arms}

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

    st.markdown("<h1 style='font-size: 36px; font-weight: bold; margin-top: 0; padding-top: 0;'>🕹️ MAB Simulation </h1>", unsafe_allow_html=True)
    # MAB 비교
    st.markdown(f"<h3 style='font-size: 22px;'>📈 MAB 알고리즘 성능 비교 ({metric} 기준)</h3>", unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(10, 3))
    ax1.plot(np.cumsum(eg_rewards), label='Epsilon-Greedy')
    ax1.plot(np.cumsum(ts_rewards), label='Thompson Sampling')
    ax1.set_title(f'Cumulative Reward ({metric}-based)')
    ax1.set_xlabel('Round')
    ax1.set_ylabel(metric)
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # A/B Test vs MAB
    st.markdown(f"<h3 style='font-size: 22px;'> 📈 A/B Test vs MAB 성능 비교 ({metric} 기준)</h3>", unsafe_allow_html=True)
    ab_rewards = []
    for t in range(n_rounds):
        arm = arms[t % 2]
        reward = np.random.binomial(1, ctr_dict[arm])
        ab_rewards.append(reward)

    fig2, ax2 = plt.subplots(figsize=(10, 3))
    ax2.plot(np.cumsum(ab_rewards), label='A/B Test (CTR)')
    ax2.plot(np.cumsum(ts_rewards), label='Thompson Sampling')
    ax2.set_title(f'MAB vs A/B Test ({metric})')
    ax2.set_xlabel('Round')
    ax2.set_ylabel('Cumulative Reward')
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
