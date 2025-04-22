import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df_main = pd.read_csv('data/merged_gapminder.csv')
    df_geo  = (
        pd.read_csv('data/ddf--entities--geo--country.csv', usecols=['country','name'])
          .rename(columns={'name':'full_name'})
    )
    df = df_main.merge(df_geo, on='country', how='left')
    df['full_name'] = df['full_name'].replace({
        'South Korea':    'Republic of Korea',
        'USA':            'United States',
        'UK':             'United Kingdom',
    })
    df['display_name'] = df['full_name']
    return df

df = load_data()

st.title("SDG 11: 인구증가·감소 Top 10 & 증감 비율 Top 10")
st.write("선택한 기간 동안 인구 증가량/감소량과 전체 인구 대비 증감 비율 Top 10 국가를 지도로 시각화합니다.")
st.markdown("---")

# 기간 선택
years = sorted(df['year'].unique())
y1, y2 = st.select_slider("기간 선택", options=years, value=(years[0], years[-1]))

# 피벗 및 변화량 계산
pop = (
    df[df.year.isin([y1, y2])]
    .pivot(index='country', columns='year', values='pop')
    .dropna()
)
pop['change'] = pop[y2] - pop[y1]
pop['pct_change'] = pop['change'] / pop[y1] * 100

# 국가 이름 매핑 (중복 제거)
country_name_map = (
    df[['country','display_name']]
    .drop_duplicates(subset='country')
    .set_index('country')['display_name']
    .to_dict()
)

pop['iso_code']     = pop.index.str.upper()
pop['display_name'] = pop.index.map(country_name_map)

### ▶ 인구증가량 Top 10
top10 = pop.sort_values('change', ascending=False).head(10).reset_index()
fig_inc = px.scatter_geo(
    top10,
    locations='iso_code',
    size='change',
    hover_name='display_name',
    projection='natural earth',
    title=f"{y1} → {y2} 인구증가량 Top 10"
)
fig_inc.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>증가량: %{marker.size:,}명"
)
st.plotly_chart(fig_inc, use_container_width=True)

### ▶ 인구감소량 Top 10
bottom10 = pop.sort_values('change', ascending=True).head(10).reset_index()
bottom10['abs_change'] = bottom10['change'].abs()
fig_dec = px.scatter_geo(
    bottom10,
    locations='iso_code',
    size='abs_change',
    hover_name='display_name',
    projection='natural earth',
    title=f"{y1} → {y2} 인구감소량 Top 10"
)
fig_dec.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>감소량: %{marker.size:,}명"
)
st.plotly_chart(fig_dec, use_container_width=True)

### ▶ 인구증가율 Top 10
top10_pct = pop.sort_values('pct_change', ascending=False).head(10).reset_index()
fig_pct_inc = px.scatter_geo(
    top10_pct,
    locations='iso_code',
    size='pct_change',
    hover_name='display_name',
    projection='natural earth',
    title=f"{y1} → {y2} 인구증가율 Top 10 (%)"
)
fig_pct_inc.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>증가율: %{marker.size:.2f}%"
)
st.plotly_chart(fig_pct_inc, use_container_width=True)

### ▶ 인구감소율 Top 10
bottom10_pct = pop.sort_values('pct_change', ascending=True).head(10).reset_index()
bottom10_pct['pct_decrease'] = bottom10_pct['pct_change'].abs()
fig_pct_dec = px.scatter_geo(
    bottom10_pct,
    locations='iso_code',
    size='pct_decrease',
    hover_name='display_name',
    projection='natural earth',
    title=f"{y1} → {y2} 인구감소율 Top 10 (%)"
)
fig_pct_dec.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>감소율: %{marker.size:.2f}%"
)
st.plotly_chart(fig_pct_dec, use_container_width=True)

with st.expander("🔍 사용 설명서"):
    st.write(
        "- 슬라이더에서 시작·종료 연도를 지정하세요.\n"
        "- 순서대로: 인구 증가량 Top10, 인구 감소량 Top10,\n"
        "  인구 증가율(%) Top10, 인구 감소율(%) Top10 지도를 확인할 수 있습니다.\n"
        "- 마우스 호버 시 국가명과 수치가 툴팁에 표시됩니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 절대 증가량과 증가율이 다른 국가들은 왜 그런 차이를 보일까요?\n"
        "2. 인구 감소율이 높은 국가의 사회적·경제적 과제는 무엇이 있을까요?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 인구 변화량과 비율을 함께 분석하여 정책 우선순위 도출하기\n"
        "- 다양한 지표(예: 경제, 환경, 보건)와 연계한 종합 보고서 작성 실습"
    )
