import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LassoCV
from econml.dml import LinearDML
from sklearn.preprocessing import StandardScaler

def show():
    st.markdown("<h1 style='font-size: 36px; font-weight: bold; margin-top: 0; padding-top: 0;'> Causal Inference </h1>", unsafe_allow_html=True)
    st.markdown(
        '''
        <div style="background-color: #F6F8FA; padding: 15px 20px; border-radius: 10px; font-size: 16px; margin-bottom: 30px; line-height: 1.7;">
            <b>분석 대상</b>:  직접 설정한 기간 중 Test 캠페인 노출 사용자<br>
            <b>공변량 통제</b>:  요일, 클릭 세그먼트 등 반영<br>
            <b>기법</b>:  Double Machine Learning (econML - LinearDML 사용)
        </div>
        ''',
        unsafe_allow_html=True
    )

    # 데이터 로드
    df = pd.read_csv("data/ab_test_result.csv")  # 파일명은 실제 위치에 맞게 조정
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d", errors="coerce")

    # 사용자 날짜 선택
    start_date, end_date = st.date_input(
        "📅 분석 기간을 선택하세요",
        value=[pd.to_datetime("2019-08-01"), pd.to_datetime("2019-08-30")],
        min_value=df['Date'].min(),
        max_value=df['Date'].max()
    )
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if st.button("📊 분석 실행"):
        # 처리 변수: 이벤트 기간 Test 캠페인에 노출된 경우
        df['T_event'] = (
            (df['Campaign Name'] == 'Test Campaign') &
            (df['Date'] >= start_date) &
            (df['Date'] <= end_date)
        ).astype(int)

        # 공변량
        X = pd.get_dummies(df[["Weekday", "Click_Segment"]], drop_first=True)

        # 결과 지표
        metrics = {
            "CTR": df["CTR"].values,
            "CVR": (df["# of Purchase"] / df["# of Website Clicks"]).fillna(0).values,
            "Revenue": df["Revenue"].values
        }

        results = {}

        for metric, Y in metrics.items():
            model = LinearDML(model_y=LassoCV(), model_t=LassoCV(), random_state=0)
            model.fit(Y, df["T_event"].values, X=X)
            ate = model.effect(X).mean()
            results[metric] = ate

        # 결과 시각화 (정규화된 값으로 시각화)

        col1, col2 = st.columns([2, 1])

        with col1:
            # 정규화
            scaler = StandardScaler()
            metric_names = list(results.keys())
            metric_values = np.array(list(results.values())).reshape(-1, 1)
            normalized_values = scaler.fit_transform(metric_values).flatten()

            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.barh(metric_names, normalized_values, color=['skyblue' if v > 0 else 'salmon' for v in normalized_values])
            ax.axvline(0, color='gray', linestyle='--')
            ax.set_xlabel("Normalized Estimated ATE")
            ax.set_title("Average Treatment Effect by Metric (Standardized)")
            st.pyplot(fig)

        with col2:
            st.markdown(
                "<div style='background-color: #F6F8FA; padding: 20px; border-radius: 12px;'>"
                                "<h5 style='text-align: center;'>📌실험결과 -  ATE 추정값</h5><br>" +
                "".join([
                    f"<p><b>{k}</b>: {'🔺' if v > 0 else '🔻'} "
                    f"{v*100:.2f}%" if k in ['CTR', 'CVR'] else 
                    f"<p><b>{k}</b>: {'🔺' if v > 0 else '🔻'} ${v:,.2f}</p><br>"
                    for k, v in results.items()
                ]) +
                "</div>",
                unsafe_allow_html=True
            )
