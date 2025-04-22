import streamlit as st

st.set_page_config(page_title="SDGs 분석 대시보드", layout="wide")
st.title("🌍 SDGs 분석 대시보드 by 석리송🎵")
st.write(
    "Gapminder 기반 데이터를 활용하여 SDGs(지속가능개발목표) 관련 10가지 주제를 시각화합니다."
)
st.markdown("---")
st.sidebar.title("페이지 네비게이션")
# Streamlit 자동 인식: /pages 폴더 내 .py 파일이 메뉴로 표시됩니다
st.sidebar.info("왼쪽 메뉴에서 주제를 선택하고, 위젯을 조작해 보세요.")
st.write("각 페이지에서는 데이터 로드, 시각화, 사용설명서, 토론 질문, 교육적 함의를 제공합니다.")
