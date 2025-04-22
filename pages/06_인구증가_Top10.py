import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드 및 country → full name 매핑
@st.cache_data
def load_data():
    df_main = pd.read_csv('data/merged_gapminder.csv')
    df_geo  = (
        pd.read_csv('data/ddf--entities--geo--country.csv', usecols=['country','name'])
          .rename(columns={'name':'full_name'})
    )
    df = df_main.merge(df_geo, on='country', how='left')
    # 예시 오버라이드(필요시 추가)
    df['full_name'] = df['full_name'].replace({
        'South Korea':    'Republic of Korea',
        'USA':            'United States',
        'UK':             'United Kingdom',
    })
    # display_name 컬럼에 이모지 추가하거나 그대로 사용
    df['display_name'] = df['full_name']
    return df

df = load_data()

st.title("SDG 11: 인구증가·감소 Top 10 국가")
st.write("선택한 기간 동안 인구 증가량 및 감소량 Top 10 국가를 지도로 시각화합니다.")
st.markdown("---")

# 기간 슬라이더
years = sorted(df['year'].unique())
y1, y2 = st.select_slider("기간 선택", options=years, value=(years[0], years[-1]))

# 피벗하여 change 계산
pop = (
    df[df.year.isin([y1, y2])]
    .pivot(index='country', columns='year', values='pop')
    .dropna()
)
pop['change'] = pop[y2] - pop[y1]

# country 코드 → ISO3, full name 매핑
pop['iso_code']     = pop.index.str.upper()
pop['display_name'] = pop.index.map(df.set_index('country')['display_name'])

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
        "- 슬라이더에서 시작 연도와 종료 연도를 조정하세요.\n"
        "- 상단 지도는 인구 증가 Top 10, 하단 지도는 인구 감소 Top 10을 보여줍니다.\n"
        "- 마우스를 올리면 국가명과 변화량이 바로 확인됩니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 인구 급증이 도시화나 자원 문제에 어떤 영향을 미칠까요?\n"
        "2. 인구 감소 국가의 사회·경제적 원인은 무엇이라고 생각하나요?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 인구 변화에 따른 정책 요구 분석\n"
        "- 지속가능한 도시·지역 계획 아이디어 제안"
    )
