# 페이지별 공통 템플릿 포함
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()

st.title("SDG 3: 전 세계 기대수명 변화")
st.write("1800년부터 2100년까지 전 세계 평균 기대수명이 어떻게 변화했는지 탐구합니다.")
st.markdown("---")

# 연도 범위 선택
start_year, end_year = st.slider(
    "연도 범위 선택", int(df.year.min()), int(df.year.max()), (2000, 2020)
)
# 선택 구간 데이터 필터링
time_series = df.groupby('year').lex.mean().reset_index()
subset = time_series[(time_series.year >= start_year) & (time_series.year <= end_year)]
# 범위 평균 계산
avg = subset.lex.mean()
st.write(f"**{start_year}년부터 {end_year}년까지 평균 기대수명:** {avg:.2f}세")

# 범위 내 시계열 그래프
fig = px.line(
    subset,
    x='year',
    y='lex',
    labels={'year':'연도','lex':'평균 기대수명(세)'},
    title=f"{start_year}~{end_year}년 기대수명 변화"
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write(
        "- 슬라이더로 시작·끝 연도를 조정하여 구간을 변경할 수 있습니다."
        "- 그래프 위에 마우스를 올리면 연도별 기대수명 수치를 확인할 수 있습니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 선택 구간에서 기대수명의 급격한 변화가 있었던 시기는 언제이며, 그 이유는 무엇일까요?"
        "2. 해당 구간 내 다른 지역(권역) 또는 소득 그룹의 변화와 비교해 보세요."
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 데이터 필터링과 통계적 평균의 개념 이해."
        "- 선택 구간의 역사적·사회적 요인 연결 탐구."
    )
