import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 3: 최고·최저 기대수명 국가 비교")
st.write(
    "선택한 연도에 기대수명이 가장 긴 5개국과 짧은 5개국을 레이더 차트로 비교합니다."
)
st.markdown("---")

df = load_data()
year = st.slider("연도 선택", int(df.year.min()), int(df.year.max()), 2020)
sub = df[df.year == year]
top5 = sub.nlargest(5,'lex')
bot5 = sub.nsmallest(5,'lex')
comp = pd.concat([top5, bot5])
fig = px.line_polar(
    comp, r='lex', theta='country', color='income_groups',
    line_close=True, title=f"{year}년 기대수명 상·하위 국가 비교"
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 연도를 변경해 나라 순위 변동을 확인하세요.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 최고 기대수명 국가의 특징은?\n"
        "2. 최저 기대수명 국가의 개선 방안은?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 보건 시스템 비교 분석.\n"
        "- 국제 보건 지원 방안 모색."
    )
