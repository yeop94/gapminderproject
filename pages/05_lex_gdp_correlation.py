import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 3&8: 기대수명 vs GDP 상관관계")
st.write(
    "모든 국가의 기대수명과 1인당 GDP 간 상관관계를 연도별 애니메이션으로 탐구합니다."
)
st.markdown("---")

df = load_data()
fig = px.scatter(
    df, x='gdp_pcap', y='lex', animation_frame='year', log_x=True,
    labels={'gdp_pcap':'1인당 GDP','lex':'기대수명'}
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 애니메이션 버튼으로 연도 흐름을 재생하세요.\n- 축 스케일 로그 여부 확인.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. GDP와 기대수명이 강한 상관관계를 보이는 이유는?\n"
        "2. 예외적인 국가 사례를 찾아보세요."
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 경제 발전과 공중보건 상관 이해.\n"
        "- 정책 우선순위 선정 토론."
    )
