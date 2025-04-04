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
    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(group_means.index, group_means.values, color=["#8EC5FC", "#FFBCBC"], width=0.4)
    ax.set_ylabel("")  # Remove y-axis label
    ax.set_facecolor("white")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color("#DDD")
    ax.spines['bottom'].set_color("#DDD")
    ax.tick_params(axis='x', colors='#888')
    ax.tick_params(axis='y', colors='#888')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='#DDD')
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.01 * yval, f"{yval*100:.1f}%", ha='center', va='bottom', fontsize=10, color='#444')
    st.pyplot(fig)

def plot_trend_line(df, metric):
    df_filtered = df.dropna(subset=["Date", metric])
    daily_avg = df_filtered.groupby(["Date", "group"])[metric].mean().reset_index()

    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.set_facecolor("white")
    colors = {"control": "#A0C4FF", "test": "#FFADAD"}
    for group in daily_avg["group"].unique():
        group_data = daily_avg[daily_avg["group"] == group]
        ax.plot(group_data["Date"], group_data[metric], label=group.capitalize(), color=colors.get(group, None), linewidth=2)

        min_idx = group_data[metric].idxmin()
        max_idx = group_data[metric].idxmax()
        latest_idx = group_data.index[-1]

        for idx in [min_idx, max_idx, latest_idx]:
            row = group_data.loc[idx]
            ax.annotate(f"{row[metric]*100:.1f}%", (row["Date"], row[metric]), textcoords="offset points", xytext=(0, -10), ha='center', fontsize=8, color='#444')

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.spines['left'].set_color("#DDD")
    ax.spines['bottom'].set_color("#DDD")
    ax.tick_params(axis='x', colors='#888')
    ax.tick_params(axis='y', colors='#888')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='#DDD')
    st.pyplot(fig)

def show_summary(df, metric):
    ctrl = df[df["group"] == "control"][metric]
    test = df[df["group"] == "test"][metric]
    uplift = (test.mean() - ctrl.mean()) / ctrl.mean() * 100
    t_stat, p_val = ttest_ind(test, ctrl)

    uplift_color = "#d33" if uplift > 0 else "#007bff"
    
    summary_html = f"""
    <div style='background-color: #F6F8FA; padding: 12px; max-width: 280px; margin: auto; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
        <div style='text-align:center'><h5 style='color:#333; font-size: 16px;'>Control Mean</h5><p style='font-size: 14px;'><b>{ctrl.mean():.4f}</b></p></div>
        <div style='text-align:center'><h5 style='color:#333; font-size: 16px;'>Test Mean</h5><p style='font-size: 14px;'><b>{test.mean():.4f}</b></p></div>
        <div style='text-align:center'><h5 style='color:#333; font-size: 16px;'>Uplift (%)</h5><p style='font-size: 14px;'><b style='color:{uplift_color}'>{uplift:.2f}%</b></p></div>
        <div style='text-align:center'><h5 style='color:#333; font-size: 16px;'>p-value</h5><p style='font-size: 14px;'><b>{p_val:.4f}</b></p></div>
    </div>
    """
    st.markdown(summary_html, unsafe_allow_html=True)

def show():
    st.markdown("<h1 style='font-size: 36px; font-weight: bold; margin-top: 0; padding-top: 0;'> A/B Test Overview</h1>", unsafe_allow_html=True)

    df = load_data()

    with st.sidebar:
        st.markdown("---")
        metric = st.selectbox("Metric Selection", ["CTR", "CVR", "Revenue", "ROAS", "CPA"])
        

    st.markdown(f"<h3 style='font-size: 20px; font-weight: 600; margin-top: 0;'>📈 {metric} Daily Performance Trend</h3>", unsafe_allow_html=True)
    plot_trend_line(df, metric)

    st.markdown(" ")
    

    col1, col2 = st.columns([2, 2])

    with col1:
        st.markdown(f"<h3 style= 'font-size: 20px; font-weight: 600; margin-top: 0;'>📊 {metric} by Group</h3>", unsafe_allow_html=True)
        plot_group_bar(df, metric)

    with col2:
        st.markdown("<h3 style='font-size: 20px; font-weight: 600; margin-top: 0;'>📋 Summary</h3>", unsafe_allow_html=True)
        show_summary(df, metric)
