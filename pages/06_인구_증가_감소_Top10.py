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

st.title("SDG 11: 인구증가·감소 Top 10 국가")
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

# 국가 코드 → 풀 네임 매핑 딕셔너리 생성 (중복 제거!)
country_name_map = (
    df[['country','display_name']]
    .drop_duplicates(subset='country')
    .set_index('country')['display_name']
    .to_dict()
)

# 매핑 적용
pop['iso_code']     = pop.index.str.upper()
pop['display_name'] = pop.index.map(country_name_map)

# ▶ 인구증가 Top10
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

# ▶ 인구감소 Top10
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

with st.expander("🔍 사용 설명서"):
    st.write(
        "- 슬라이더로 시작·종료 연도를 지정하세요.\n"
        "- 상단 지도는 인구 증가 Top10, 하단 지도는 인구 감소 Top10을 보여줍니다.\n"
        "- 마우스 호버 시 국가명과 변화량이 표시됩니다."
    )
