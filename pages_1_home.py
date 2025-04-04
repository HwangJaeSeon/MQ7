import streamlit as st

def show():
    st.title(" A/B테스트 실험개요")

    col1, col2 = st.columns([1, 2])  # 왼쪽: 이미지, 오른쪽: 실험 개요

    with col1:
        st.image("bts.png", 
                 caption="A/B testing illustration", use_container_width=True)

    with col2:
        st.subheader("🎯 백투스쿨 광고 캠페인 A/B 테스트")
        st.markdown("""
- **기간**: 2019년 8월 1일 ~ 8월 30일  
- **목적**: 8월 백투스쿨 세일에 맞춰 광고 수익률(ROAS) 및 커머스 전체 이익(Revenue) 향상  
- **방식**: 무작위 A/B 테스트  
- **집단 구성**:  
    - Control 그룹: 기존 광고 캠페인  
    - Test 그룹: 신규 광고 소재 및 타겟팅 전략  
- **트래픽 분배**: 균등 랜덤 분배
        """)

        st.success("본 실험은 광고 효율을 높이기 위한 전략적 테스트로, 아래 탭에서 세부 결과를 확인할 수 있습니다.")