import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()

st.title("SDG 3: 최고·최저 기대수명 국가 비교")
st.write(
    "선택한 두 연도의 기대수명이 가장 긴(상위) 5개국과 짧은(하위) 5개국을 전체 이름으로 레이더 차트 비교합니다."
)
st.markdown("---")

# 기간 선택: 시작 및 종료 연도
y1, y2 = st.select_slider(
    "비교할 기간 선택", options=sorted(df.year.unique()), value=(2000, 2020)
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
    # country->name mapping 시 중복 제거
    country_name_map = df[['country','name']].drop_duplicates().set_index('country')['name']
    combined['name'] = combined['country'].map(country_name_map)
    return combined

comp1 = get_top_bottom(y1)
comp2 = get_top_bottom(y2)
comp = pd.concat([comp1, comp2])

# 레이더 차트 생성
fig = px.line_polar(
    comp,
    r='lex',
    theta='name',
    color='rank',
    facet_col='year',
    line_close=True,
    labels={'lex':'기대수명(세)', 'name':'국가'},
    title=f"{y1}년 vs {y2}년 기대수명 상·하위 국가 비교"
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))

st.plotly_chart(fig, use_container_width=True)

# 부가 정보
with st.expander("🔍 사용 설명서 설명 보기"):
    st.write(
        "- 슬라이더로 두 연도를 선택하세요.
"
        "- 포인터를 올리면 국가 전체 이름과 기대수명 수치를 확인합니다.
"
        "- 범례 클릭으로 Top/Bottom 구분 강조 가능합니다."
    )
with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 두 시점 간 기대수명 순위 변화의 주요 원인은 무엇일까요?
"
        "2. 상·하위 국가의 보건 정책 차이를 비교 분석해 보세요."
    )
with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 시간에 따른 복지 개선 효과를 시각적으로 이해합니다.
"
        "- 기대수명 격차 해소를 위한 정책 제안 및 모의 시뮬레이션을 진행해 봅니다."
    )
```python
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()

st.title("SDG 3: 최고·최저 기대수명 국가 비교")
st.write("선택한 두 연도의 기대수명이 가장 긴/짧은 5개국을 전체 이름으로 레이더 차트 비교합니다.")
st.markdown("---")

y1, y2 = st.select_slider(
    "비교할 기간 선택", options=sorted(df.year.unique()), value=(2000, 2020)
)

def get_top_bottom(year):
    sub = df[df.year == year]
    top5 = sub.nlargest(5, 'lex')[['country','lex','income_groups']]
    bottom5 = sub.nsmallest(5, 'lex')[['country','lex','income_groups']]
    top5['rank'] = 'Top 5'
    bottom5['rank'] = 'Bottom 5'
    combined = pd.concat([top5, bottom5])
    combined['year'] = year
    combined['name'] = combined['country'].map(df.set_index('country')['name'])
    return combined

comp1 = get_top_bottom(y1)
comp2 = get_top_bottom(y2)
comp = pd.concat([comp1, comp2])

fig = px.line_polar(
    comp,
    r='lex',
    theta='name',
    color='rank',
    facet_col='year',
    line_close=True,
    labels={'lex':'기대수명(세)', 'name':'국가'},
    title=f"{y1}년 vs {y2}년 기대수명 상·하위 국가 비교"
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write("- 슬라이더로 두 연도 선택.
- 마우스 오버로 전체 국가 이름과 값 확인.")
with st.expander("💡 학생 토론 질문"):
    st.markdown("1. 기대수명 순위 변동 원인은?
2. 국가별 정책 차이 분석?")
with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write("- 보건 정책 효과 시각화.
- 모의 정책 설계 실습.")
```python
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/merged_gapminder.csv')

df = load_data()

st.title("SDG 3: 최고·최저 기대수명 국가 비교")
st.write(
    "선택한 두 연도의 기대수명이 가장 긴(상위) 5개국과 짧은(하위) 5개국을 레이더 차트로 비교합니다."
)
st.markdown("---")

# 기간 선택: 시작 연도와 종료 연도
y1, y2 = st.select_slider(
    "비교할 기간 선택", options=sorted(df.year.unique()), value=(2000, 2020)
)

# 각 연도별 상위·하위 5개국 추출
def get_top_bottom(year):
    sub = df[df.year == year]
    top5 = sub.nlargest(5, 'lex')[['country','lex','income_groups']]
    bottom5 = sub.nsmallest(5, 'lex')[['country','lex','income_groups']]
    top5['rank'] = 'Top 5'
    bottom5['rank'] = 'Bottom 5'
    combined = pd.concat([top5, bottom5])
    combined['year'] = year
    return combined

comp1 = get_top_bottom(y1)
comp2 = get_top_bottom(y2)
comp = pd.concat([comp1, comp2])

# 레이더 차트: facet_col으로 연도별 비교
fig = px.line_polar(
    comp,
    r='lex',
    theta='country',
    color='rank',
    facet_col='year',
    line_close=True,
    labels={'lex':'기대수명(세)'},
    title=f"{y1}년 vs {y2}년 국가별 기대수명 상·하위 비교"
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 사용 설명서 설명 보기"):
    st.write(
        "- 슬라이더를 움직여 두 연도를 선택하세요."
        "- 각 연도의 레이더 차트에서 상·하위 국가 분포를 비교할 수 있습니다."
        "- 범례에서 Top/Bottom을 클릭해 강조할 수 있습니다."
    )
with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 두 시점 간 기대수명 순위 변동의 원인은 무엇일까요?"
        "2. 최상·최하위 국가의 정책 차이를 분석해보세요."
    )
with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 시간에 따른 복지 개선 효과를 시각적으로 이해합니다."
        "- 모의 정책 제안을 통해 기대수명 향상 전략을 구상해 봅니다."
    )
