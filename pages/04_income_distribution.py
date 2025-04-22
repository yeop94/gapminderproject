import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 10: 소득그룹별 1인당 GDP 분포")
st.write(
    "소득 그룹별 1인당 GDP 분포를 연도별 박스 플롯으로 비교합니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()
years = st.multiselect("연도 선택", options=sorted(df.year.unique()), default=[2000,2020])
sub = df[df.year.isin(years)]
fig = px.box(sub, x='income_groups', y='gdp_pcap', color='year', labels={'gdp_pcap':'1인당 GDP'})
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 멀티셀렉트로 비교할 연도를 선택하세요.\n- 박스 플롯의 분포와 이상치 주목.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 소득 불평등이 사회에 미치는 영향은?\n"
        "2. 소득 그룹 간 이동성이 있나요?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 사회경제적 격차 이해.\n"
        "- 불평등 해소를 위한 정책 제안."
    )
