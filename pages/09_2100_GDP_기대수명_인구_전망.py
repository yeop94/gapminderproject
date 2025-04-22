import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 8: 국가별 GDP·기대수명·인구 비교 (기간 선택 가능)")
st.write(
    "다중 선택과 기간 슬라이더를 통해 여러 국가의 경제·보건·인구 지표를 비교할 수 있습니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    df_main = pd.read_csv('data/merged_gapminder.csv')
    df_geo  = pd.read_csv(
        'data/ddf--entities--geo--country.csv',
        usecols=['country','name']
    ).rename(columns={'name':'full_name'})
    df = df_main.merge(df_geo, on='country', how='left')
    # 이름 오버라이드
    df['full_name'] = df['full_name'].replace({
        'South Korea':       'Republic of Korea',
        'USA':               'United States',
        'UK':                'United Kingdom',
    })
    # 국기 이모지
    flags = {
        'United States':     '🇺🇸',
        'China':             '🇨🇳',
        'India':             '🇮🇳',
        'Japan':             '🇯🇵',
        'Germany':           '🇩🇪',
        'United Kingdom':    '🇬🇧',
        'Republic of Korea': '🇰🇷',
        'France':            '🇫🇷',
        'Brazil':            '🇧🇷',
        'Canada':            '🇨🇦',
        'Australia':         '🇦🇺'
    }
    df['display_name'] = df['full_name'].apply(
        lambda n: f"{flags[n]} {n}" if n in flags else n
    )
    return df

# 데이터 로드
df = load_data()
min_year, max_year = int(df['year'].min()), int(df['year'].max())

# 사이드바: 기간 선택
st.sidebar.markdown("### ⏳ 기간 선택")
year_start, year_end = st.sidebar.slider(
    "비교할 연도 범위",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

# 사이드바: 국가 다중 선택
major = [
    f"{emoji} {name}" for name, emoji in [
        ("United States", "🇺🇸"),
        ("China", "🇨🇳"),
        ("India", "🇮🇳"),
        ("Japan", "🇯🇵"),
        ("Germany", "🇩🇪"),
        ("United Kingdom", "🇬🇧"),
        ("Republic of Korea", "🇰🇷"),
        ("France", "🇫🇷"),
        ("Brazil", "🇧🇷"),
        ("Canada", "🇨🇦"),
        ("Australia", "🇦🇺")
    ]
]
all_countries = sorted(df['display_name'].unique())
others = [c for c in all_countries if c not in major]
options = major + others

st.sidebar.markdown("### 🌍 국가 선택")
selected = st.sidebar.multiselect(
    "최소 1개 이상 선택하세요",
    options=options,
    default=[major[6]]  # 🇰🇷 Republic of Korea
)

if not selected:
    st.sidebar.warning("하나 이상의 국가를 선택해야 합니다.")
    st.stop()

# 필터링: 국가 + 연도 범위
df_sel = df[
    (df['display_name'].isin(selected)) &
    (df['year'] >= year_start) &
    (df['year'] <= year_end)
]

# 1인당 GDP 그래프
fig_gdp = px.line(
    df_sel, x='year', y='gdp_pcap', color='display_name',
    labels={'gdp_pcap':'1인당 GDP (USD)', 'year':'연도', 'display_name':'국가'},
    title=f"1인당 GDP ({year_start}–{year_end}) 비교"
)
st.plotly_chart(fig_gdp, use_container_width=True)

# 기대수명 그래프
fig_lex = px.line(
    df_sel, x='year', y='lex', color='display_name',
    labels={'lex':'기대수명 (년)', 'year':'연도', 'display_name':'국가'},
    title=f"기대수명 ({year_start}–{year_end}) 비교"
)
st.plotly_chart(fig_lex, use_container_width=True)

# 인구 수 그래프
fig_pop = px.line(
    df_sel, x='year', y='pop', color='display_name',
    labels={'pop':'인구 수', 'year':'연도', 'display_name':'국가'},
    title=f"인구 수 ({year_start}–{year_end}) 비교"
)
st.plotly_chart(fig_pop, use_container_width=True)

with st.expander("🔍 사용 설명서"):
    st.write(
        f"- 사이드바에서 연도 범위를 {year_start}년부터 {year_end}년으로 설정할 수 있습니다.\n"
        "- 다중 선택으로 비교하고 싶은 국가를 지정하세요."
    )

with st.expander("💡 토론 질문"):
    st.markdown(
        "1. 선택한 기간 동안 국가 간 성장 추세 차이는 무엇이 원인일까요?\n"
        "2. 인구 변화가 GDP·기대수명에 미친 영향을 분석해 보세요."
    )
