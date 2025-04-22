import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 8: 여러 국가의 2050년까지 GDP · 기대수명 · 인구 비교")
st.write(
    "다중 선택을 통해 주요 국가뿐 아니라 전 세계 국가들의 1인당 GDP, 기대수명, 인구 변화를 비교할 수 있습니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    df_main = pd.read_csv('data/merged_gapminder.csv')
    df_geo  = pd.read_csv('data/ddf--entities--geo--country.csv', usecols=['country','name'])
    df_geo  = df_geo.rename(columns={'name':'full_name'})
    df = df_main.merge(df_geo, on='country', how='left')
    override = {
        'South Korea':       'Republic of Korea',
        'USA':               'United States',
        'UK':                'United Kingdom',
    }
    df['full_name'] = df['full_name'].replace(override)
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

df = load_data()

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

st.sidebar.markdown("### 🌍 비교할 국가 선택")
selected = st.sidebar.multiselect(
    "최소 1개 이상의 국가를 선택하세요",
    options=options,
    default=[major[6]]  # 🇰🇷 Republic of Korea
)

if not selected:
    st.sidebar.warning("하나 이상의 국가를 선택해야 그래프를 표시합니다.")
    st.stop()

df_sel = df[
    df['display_name'].isin(selected) &
    (df['year'] <= 2050)
]

# 1인당 GDP 비교
fig_gdp = px.line(
    df_sel, x='year', y='gdp_pcap', color='display_name',
    labels={'gdp_pcap':'1인당 GDP (USD)', 'year':'연도', 'display_name':'국가'},
    title="1인당 GDP 전망 비교"
)
st.plotly_chart(fig_gdp, use_container_width=True)

# 기대수명 비교
fig_lex = px.line(
    df_sel, x='year', y='lex', color='display_name',
    labels={'lex':'기대수명 (년)', 'year':'연도', 'display_name':'국가'},
    title="기대수명 전망 비교"
)
st.plotly_chart(fig_lex, use_container_width=True)

# 인구 수 비교
fig_pop = px.line(
    df_sel, x='year', y='pop', color='display_name',
    labels={'pop':'인구 수', 'year':'연도', 'display_name':'국가'},
    title="인구 수 전망 비교"
)
st.plotly_chart(fig_pop, use_container_width=True)

with st.expander("🔍 사용 설명서"):
    st.write(
        "- 사이드바에서 최소 하나의 국가를 선택하세요 (기본값: 🇰🇷 Republic of Korea).\n"
        "- 선택된 국가들의 1800~2050년 범위 데이터를 한 눈에 비교할 수 있습니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 인구 변화와 GDP·기대수명 간에는 어떤 상관관계가 있을까?\n"
        "2. 인구 폭발 또는 감소가 경제·건강 지표에 미치는 영향을 예측해 보세요."
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 인구·경제·보건 지표를 통합해 시나리오 모델링 실습\n"
        "- 그룹별(대륙·소득 수준) 비교 분석 및 정책 제안"
    )
