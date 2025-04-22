import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()

st.title("SDG 3: 최고·최저 기대수명 국가 비교")
st.write("두 시점의 기대수명이 가장 긴 5개국과 가장 짧은 5개국을 전체 이름으로 레이더 차트로 비교합니다.")
st.markdown("---")

# 기간 선택: 시작 및 종료 연도
y1, y2 = st.select_slider(
    "비교할 연도 선택", options=sorted(df.year.unique()), value=(2000, 2020)
)

# 연도별 데이터 추출
def get_top_bottom(year):
    sub = df[df.year == year]
    top5 = sub.nlargest(5, 'lex')[['country', 'lex', 'income_groups']]
    bottom5 = sub.nsmallest(5, 'lex')[['country', 'lex', 'income_groups']]
    top5['rank'] = 'Top 5'
    bottom5['rank'] = 'Bottom 5'
    combined = pd.concat([top5, bottom5])
    # country->name 매핑
    name_map = df[['country','name']].drop_duplicates().set_index('country')['name']
    combined['name'] = combined['country'].map(name_map)
    return combined

# 데이터 생성
data1 = get_top_bottom(y1)
data2 = get_top_bottom(y2)

# 두 차트를 나란히 배치\ ncols = st.columns(2)
col1, col2 = ncols
fig1 = px.line_polar(
    data1,
    r='lex', theta='name', color='rank', line_close=True,
    labels={'lex':'기대수명(세)','name':'국가'},
    title=f"{y1}년 기대수명 Top/Bottom"
)
fig2 = px.line_polar(
    data2,
    r='lex', theta='name', color='rank', line_close=True,
    labels={'lex':'기대수명(세)','name':'국가'},
    title=f"{y2}년 기대수명 Top/Bottom"
)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write(
        "- 슬라이더로 두 연도를 선택하고 차트를 비교하세요."
        "- 마우스 오버로 국가 이름과 기대수명을 확인합니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 각 시점 Top/Bottom 국가 구성 차이를 설명해 보세요."
        "2. 순위 변화 원인을 토의해 보세요."
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 정책 효과를 시각적으로 비교합니다."
        "- 정책 개선 아이디어를 제안해 보세요."
    )
