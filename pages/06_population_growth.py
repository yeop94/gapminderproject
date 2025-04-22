import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()

st.title("SDG 11: 인구증가 상위 10개국")
st.write(
    "선택한 기간 동안 인구 증가량이 가장 큰 상위 10개국을 지도로 시각화합니다."
)
st.markdown("---")

y1, y2 = st.select_slider(
    "기간 선택", options=sorted(df.year.unique()), value=(2000, 2020)
)
# 인구 변화 계산 및 상위 10개국 추출
pop = df[df.year.isin([y1, y2])].pivot(
    index='country', columns='year', values='pop'
).dropna()
pop['change'] = pop[y2] - pop[y1]
top10 = pop.sort_values('change', ascending=False).head(10).reset_index()
# ISO-3 코드 대문자로 변환하여 지도 매핑
top10['iso_code'] = top10['country'].str.upper()

fig = px.scatter_geo(
    top10,
    locations='iso_code',
    size='change',
    projection='natural earth',
    title=f"{y1} → {y2} 인구증가량 Top10"
)
fig.update_traces(
    hovertemplate="국가: %{location}<br>증가량: %{marker.size:,}명"
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write(
        "- 기간 슬라이더로 시작 연도와 종료 연도를 설정합니다.
"
        "- 지도 위 원의 크기가 인구 증가량을 나타냅니다.
"
        "- 원 위로 마우스를 올리면 국가 코드와 증가량을 확인할 수 있습니다."
    )
with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 인구 급증이 환경과 도시화에 미치는 영향은 무엇일까요?"
        "2. 인구가 감소하는 국가의 사례와 원인은 무엇인가요?"
    )
with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 인구 변화의 경제·사회적 영향 분석."
        "- 지속가능한 도시 계획 아이디어 제안."
    )
