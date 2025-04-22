import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 13: 소득그룹별 1인당 GDP 추세")
st.write(
    "소득그룹별 평균 1인당 GDP 변화를 선그래프로 비교합니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()
groups = df.groupby(['year','income_groups']).gdp_pcap.mean().reset_index()
fig = px.line(
    groups, x='year', y='gdp_pcap', color='income_groups',
    labels={'gdp_pcap':'평균 1인당 GDP'}
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 범례 클릭으로 그룹 선택/비활성화.\n- 그래프 확대 기능 활용.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 소득그룹 간 성장 격차 원인은?\n"
        "2. 중저소득 국가의 성장 가능성은?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 경제적 불균형과 정책 대안 모색.\n"
        "- 국제 개발 협력 방안 토론."
    )
