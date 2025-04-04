from streamlit_option_menu import option_menu
import streamlit as st

def show_sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title= "TORI COMMERCE",  # 메뉴 타이틀
            options=["실험개요", "A/B테스트 결과", "인과추론 결과", "MAB 시뮬레이션"],
            icons=["house", "bar-chart", "activity", "shuffle"],
            default_index=0,
            styles={
                "container": {
                    "padding": "10px",
                    "background-color": "#F5F7FA",  # 연회색 배경
                },
                "icon": {
                    "color": "#5A5A5A",  # 기본 아이콘 색상
                    "font-size": "18px"
                },
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px 0",
                    "--hover-color": "#E0E6ED",  # hover 시 밝은 회색
                    "color": "#333333",
                    "border-radius": "8px"
                },
                "nav-link-selected": {
                    "background-color": "#0066FF",  # 파란색 선택 배경
                    "color": "white",
                    "font-weight": "bold"
                } 
            }
        )

        # 메뉴 아래 사용자 정보 
        st.markdown("---")
        st.markdown("👏 Team C1 ")
        st.markdown("🗓️ 2025.4.7")

        return selected