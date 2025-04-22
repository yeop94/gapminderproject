import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()

st.title("SDG 3&8: 기대수명 vs GDP 상관관계")
st.write(
    "모든 국가의 기대수명과 1인당 GDP 간 상관관계를 연도별 애니메이션으로 탐구합니다."
)
st.markdown("---")

fig = px.scatter(
    df,
    x='gdp_pcap',
    y='lex',
    animation_frame='year',
    animation_group='country',
    log_x=True,
    size_max=45,
    hover_name='country',
    hover_data={'year': True, 'gdp_pcap':':,.2f', 'lex':':.2f'},
    labels={'gdp_pcap':'1인당 GDP','lex':'기대수명'},
    title="기대수명↔GDP 상관관계"
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write(
        "- 애니메이션 재생 버튼으로 연도별 변화를 확인하세요."
        "- 각 점 위로 마우스를 올려 국가, 연도, GDP, 기대수명을 정확히 확인할 수 있습니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 특정 연도의 상관관계 패턴은 어떻게 변했나요?"
        "2. 예외적인 국가(높거나 낮은 기대수명 대비 GDP)를 찾아 분석해보세요."
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 경제발전과 공중보건의 상관성을 시각적으로 이해합니다."
        "- 정책 결정 시 데이터를 활용한 근거 마련 방법을 학습합니다."
    )
