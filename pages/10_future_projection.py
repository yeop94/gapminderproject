import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 8: 2050년까지 GDP·기대수명 전망")
st.write(
    "기존 데이터를 바탕으로 2050년까지 전 세계 평균 1인당 GDP와 기대수명 변화를 시각화합니다."
)
st.markdown("---")

df = load_data()
future = df[df.year <= 2050].groupby('year').agg({'gdp_pcap':'mean','lex':'mean'}).reset_index()
fig1 = px.line(future, x='year', y='gdp_pcap', labels={'gdp_pcap':'평균 1인당 GDP'}, title='GDP 전망')
fig2 = px.line(future, x='year', y='lex', labels={'lex':'평균 기대수명'}, title='기대수명 전망')
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 슬라이더 없이 자동으로 2050년까지 추세를 표시합니다.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 미래 전망을 어떻게 활용할 수 있을까?\n"
        "2. SDG 달성을 위한 장기 계획은?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 데이터 기반 예측의 한계와 가능성 이해.\n"
        "- 정책 시나리오 계획 실습."
    )
