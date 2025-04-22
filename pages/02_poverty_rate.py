import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 1: 저소득 국가 비율 변화")
st.write(
    "연도별로 1인당 GDP 기준 저소득 국가(기본 1000 USD 미만)가 차지하는 비율을 분석합니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()
threshold = st.number_input("저소득 기준 (USD)", value=1000)
low_pct = df.groupby('year').apply(
    lambda x: (x.gdp_pcap < threshold).mean()*100
).reset_index(name='pct')
fig = px.area(low_pct, x='year', y='pct', labels={'pct':'저소득 국가 비율(%)'})
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 기준값을 조정하여 변화 추이를 확인하세요.\n- 영역 차트 위 마우스 오버로 연도별 비율 조회.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 빈곤 기준을 높이면 결과는 어떻게 달라질까?\n"
        "2. 특정 지역의 빈곤 감소 사례를 찾아보세요."
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 빈곤 정의와 기준의 다양성 이해.\n"
        "- 글로벌 빈곤 퇴치 정책 토론."
    )
