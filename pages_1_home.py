import streamlit as st

def show():
    st.title(" 😸 토리커머스 마케팅캠페인 A/B테스트 ")
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, spacer, col2 = st.columns([2.3 , 0.001, 5])  # 왼쪽: 이미지, 오른쪽: 실험 개요

    with col1:
        st.image("bts.png", 
                 caption="A/B testing illustration", use_container_width=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

    with col2:
        st.subheader("🎯 백투스쿨 광고 캠페인 ")
        st.markdown("""
        <span style='background-color:#f0f2f6; padding:4px 8px; border-radius:6px; font-weight:bold;'>기간</span> 2019년 8월 1일 ~ 8월 30일  

        <span style='background-color:#f0f2f6; padding:4px 8px; border-radius:6px; font-weight:bold;'>목적</span> 세일에 맞춰 광고 수익률(ROAS) 및 커머스 전체 이익(Revenue) 향상  
        
        <span style='background-color:#f0f2f6; padding:4px 8px; border-radius:6px; font-weight:bold;'>방식</span> 무작위 A/B 테스트  
        
        <span style='background-color:#f0f2f6; padding:4px 8px; border-radius:6px; font-weight:bold;'>집단 구성</span> [Control/Test] 기존 광고 캠페인/신규 광고 소재 및 타겟팅 전략  
        
        <span style='background-color:#f0f2f6; padding:4px 8px; border-radius:6px; font-weight:bold;'>트래픽 분배</span> 균등 랜덤 분배
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
        st.success("본 실험은 광고 효율을 높이기 위한 전략적 테스트로, 아래 탭에서 세부 결과를 확인할 수 있습니다.", icon="ℹ️")