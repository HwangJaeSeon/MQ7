
import streamlit as st
from pages_1_home import show as show_home
from pages_2_ABtest import show as show_ABtest
from pages_3_Causal_Inference import show as show_Causal_Inference
from pages_4_MAB import show as show_MAB  # ⬅️ 이 줄 추가!

from components.sidebar import show_sidebar

# 사이드바
page = show_sidebar()

# 페이지 라우팅
if page == "실험개요":
    show_home()
elif page == "A/B테스트 결과":
    show_ABtest()
elif page == "인과추론 결과":
    show_Causal_Inference()
elif page == "MAB 시뮬레이션":  # ⬅️ 이 부분도 추가!
    show_MAB()