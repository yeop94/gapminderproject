import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 11: 인구증가 상위 10개국")
st.write(
    "선택한 기간 동안 인구 증가량이 가장 큰 상위 10개국을 지도에 표시합니다."
)
st.markdown("---")

df = load_data()
y1, y2 = st.select_slider("기간 선택", options=sorted(df.year.unique()), value=(2000,2020))
pop = df[df.year.isin([y1,y2])].pivot(index='country', columns='year', values='pop').dropna()
pop['change'] = pop[y2] - pop[y1]
top10 = pop.sort_values('change', ascending=False).head(10).reset_index()
fig = px.scatter_geo(
    top10, locations='country', locationmode='ISO-3', size='change',
    projection='natural earth', title=f"{y1}→{y2} 인구증가량 Top10"
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 기간 슬라이더로 시작/끝 연도를 설정하세요.\n- 지도에서 원 크기가 증가량을 나타냅니다.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 인구 급증이 환경에 미치는 영향은?\n"
        "2. 급감 사례와 원인은?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 인구구조 변화와 사회 문제 분석.\n"
        "- 지속가능한 도시 계획 모의 설계."
    )
