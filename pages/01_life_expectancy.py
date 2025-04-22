import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 3: 전 세계 기대수명 변화")
st.write(
    "1800년부터 2100년까지 전 세계 평균 기대수명이 어떻게 변화했는지 탐구합니다."
)
st.markdown("---")

df = load_data()

year = st.slider("연도 선택", int(df.year.min()), int(df.year.max()), 2000)
avg = df[df.year == year].lex.mean()
st.write(f"**{year}년 전 세계 평균 기대수명:** {avg:.2f}세")
time_series = df.groupby('year').lex.mean().reset_index()
fig = px.line(time_series, x='year', y='lex', labels={'year':'연도','lex':'평균 기대수명(세)'})
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write(
        "- 슬라이더를 통해 연도를 변경해 보세요.\n"
        "- 그래프 위에 마우스를 올리면 세부값이 표시됩니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 19세기 말 기대수명이 낮았던 이유는?\n"
        "2. 주요 전염병이 기대수명에 미친 영향은?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 역사적 사건과 보건 정책 연계 분석.\n"
        "- 기대수명 격차 해소를 위한 정책 제안."
    )
