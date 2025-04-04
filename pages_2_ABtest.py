import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/ab_test_result.csv")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["group"] = df["Campaign Name"].apply(lambda x: "control" if "Control" in x else "test")
    return df

def plot_group_bar(df, metric):
    group_means = df.groupby("group")[metric].mean()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.bar(group_means.index, group_means.values, color=["skyblue", "salmon"])
    ax.set_title(f"{metric} by Group")
    ax.set_ylabel(metric)
    st.pyplot(fig)

def plot_trend_line(df, metric):
    df_filtered = df.dropna(subset=["Date", metric])
    daily_avg = df_filtered.groupby(["Date", "group"])[metric].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 2.5))
    for group in daily_avg["group"].unique():
        group_data = daily_avg[daily_avg["group"] == group]
        ax.plot(group_data["Date"], group_data[metric], label=group)

    ax.set_title(f"{metric} Daily Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel(metric)
    ax.legend()
    st.pyplot(fig)

def show_summary(df, metric):
    ctrl = df[df["group"] == "control"][metric]
    test = df[df["group"] == "test"][metric]
    uplift = (test.mean() - ctrl.mean()) / ctrl.mean() * 100
    t_stat, p_val = ttest_ind(test, ctrl)

    uplift_color = "#d33" if uplift > 0 else "#007bff"
    
    summary_html = f"""
    <div style='background-color: #F6F8FA; padding: 16px; border-radius: 12px;'>
        <div style='text-align:center'><h5 style='color:#333; font-size: 16px;'>Control Mean</h5><p style='font-size: 14px;'><b>{ctrl.mean():.4f}</b></p></div>
        <div style='text-align:center'><h5 style='color:#333; font-size: 16px;'>Test Mean</h5><p style='font-size: 14px;'><b>{test.mean():.4f}</b></p></div>
        <div style='text-align:center'><h5 style='color:#333; font-size: 16px;'>Uplift (%)</h5><p style='font-size: 14px;'><b style='color:{uplift_color}'>{uplift:.2f}%</b></p></div>
        <div style='text-align:center'><h5 style='color:#333; font-size: 16px;'>p-value</h5><p style='font-size: 14px;'><b>{p_val:.4f}</b></p></div>
    </div>
    """
    st.markdown(summary_html, unsafe_allow_html=True)

def show():
    st.markdown("<h1 style='font-size: 36px; font-weight: bold; margin-top: 0; padding-top: 0;'>📊 A/B Test Overview</h1>", unsafe_allow_html=True)

    df = load_data()

    with st.sidebar:
        st.markdown("---")
        metric = st.selectbox("지표 선택", ["CTR", "CVR", "Revenue", "ROAS", "CPA"])

    col_center, _, col_right = st.columns([2, 0.2, 2])

    with col_center:
        st.markdown("<h3 style='font-size: 22px; font-weight: 600; margin-top: 0;'>✅ 그룹 평균 비교</h3>", unsafe_allow_html=True)
        plot_group_bar(df, metric)

    with col_right:
        st.markdown("<h3 style='font-size: 22px; font-weight: 600; margin-top: 0;'>✅ 통계요약</h3>", unsafe_allow_html=True)
        st.markdown("  ")
        show_summary(df, metric)

    st.markdown("<h3 style='font-size: 22px; font-weight: 600; margin-top: 0;'>📅 날짜별 추이</h3>", unsafe_allow_html=True)
    plot_trend_line(df, metric)
