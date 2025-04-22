import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 1&10: 권역별 저소득 국가 수 변화")
st.write(
    "권역별로 기준 미만 1인당 GDP 국가 수의 연도별 변화를 면적차트로 표시합니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()
threshold = st.number_input("저소득 기준 (USD)", value=1000)
low = df[df.gdp_pcap < threshold]
count = low.groupby(['year','world_4region']).country.nunique().reset_index(name='count')
fig = px.area(
    count, x='year', y='count', color='world_4region',
    labels={'count':'국가 수'}
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 기준값을 변경하며 국가 수 변화를 살펴보세요.\n- 특정 권역 클릭으로 강조.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 특정 권역의 빈곤 감소 사례는?\n"
        "2. 권역별 개발 협력 전략은?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 지역 간 격차 분석.\n"
        "- 다자 개발 은행 역할 토론."
    )
