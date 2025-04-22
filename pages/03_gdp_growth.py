import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 8: GDP 성장률 Top10 국가 비교")
st.write(
    "선택한 기간 동안 GDP 성장률이 높은 상위 10개국을 비교합니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()
y1, y2 = st.select_slider(
    "기간 선택", options=sorted(df.year.unique()), value=(2000,2020)
)
sub = df[df.year.isin([y1,y2])].pivot(index='country', columns='year', values='gdp_pcap').dropna()
sub['growth'] = (sub[y2]-sub[y1]) / sub[y1] * 100
top10 = sub.sort_values('growth', ascending=False).head(10).reset_index()
fig = px.bar(top10, x='country', y='growth', labels={'growth':'성장률(%)'})
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 슬라이더로 시작 연도와 종료 연도를 설정하세요.\n- 막대 위 마우스 오버로 성장률 확인.")

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 성장률이 높은 국가가 지속가능한 이유는?\n"
        "2. GDP 성장과 SDG 달성 간 연관성은?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 경제성장과 사회적 영향 분석.\n"
        "- 성장 전략 모의 정책 설계."
    )
