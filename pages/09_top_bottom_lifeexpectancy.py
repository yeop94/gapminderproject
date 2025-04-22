import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()

st.title("SDG 3: 최고·최저 기대수명 국가 비교")
st.write(
    "두 시점의 기대수명이 가장 긴 5개국(Top 5)과 가장 짧은 5개국(Bottom 5)을 국가 전체 이름으로 레이더 차트 비교합니다."
)
st.markdown("---")

# 기간 선택: 시작 및 종료 연도
y1, y2 = st.select_slider(
    "비교할 연도 선택", options=sorted(df.year.unique()), value=(2000, 2020)
)

# 연도별 상위/하위 국가 데이터 생성
def get_top_bottom(year):
    sub = df[df.year == year]
    top5 = sub.nlargest(5, 'lex')[['country', 'lex', 'income_groups']]
    bottom5 = sub.nsmallest(5, 'lex')[['country', 'lex', 'income_groups']]
    top5['rank'] = 'Top 5'
    bottom5['rank'] = 'Bottom 5'
    combined = pd.concat([top5, bottom5])
    combined['year'] = year
    # country->name 매핑
    name_map = df[['country','name']].drop_duplicates().set_index('country')['name']
    combined['name'] = combined['country'].map(name_map)
    return combined

comp1 = get_top_bottom(y1)
comp2 = get_top_bottom(y2)
comp = pd.concat([comp1, comp2])
# year를 문자열로 변환하여 facet 문자열 처리
tmp = comp.copy()
tmp['year'] = tmp['year'].astype(str)

# 레이더 차트 생성
fig = px.line_polar(
    tmp,
    r='lex',
    theta='name',
    color='rank',
    facet_col='year',
    facet_col_wrap=2,
    line_close=True,
    labels={'lex':'기대수명(세)', 'name':'국가'},
    title=f"{y1}년 vs {y2}년 기대수명 상·하위 비교"
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))

st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write(
        "- 슬라이더로 두 연도를 선택하세요."
        "- 포인터를 올리면 국가 이름과 기대수명 값을 확인할 수 있습니다."
        "- 범례에서 Top/Bottom을 클릭해 강조할 수 있습니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 두 시점 간 기대수명 순위가 어떻게 달라졌나요?"
        "2. 상·하위 국가 보건 정책의 차이점을 토의해 보세요."
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 복지 정책이 기대수명에 미친 영향을 시각적으로 이해합니다."
        "- 기대수명 향상 전략을 팀별로 설계해 봅니다."
    )
