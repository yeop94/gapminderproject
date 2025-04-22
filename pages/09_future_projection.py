import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 8: 여러 국가의 2050년까지 GDP · 기대수명 비교")
st.write(
    "다중 선택을 통해 주요 국가뿐 아니라 전 세계 국가들의 1인당 GDP와 기대수명 변화를 비교할 수 있습니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    # 1) 시계열 데이터 로드
    df_main = pd.read_csv('data/merged_gapminder.csv')
    # 2) ISO→풀네임 매핑
    df_geo = pd.read_csv('data/ddf--entities--geo--country.csv', usecols=['country','name'])
    df_geo = df_geo.rename(columns={'name':'full_name'})
    df = df_main.merge(df_geo, on='country', how='left')
    # 3) 네이밍 오버라이드
    override = {
        'South Korea':       'Republic of Korea',
        'USA':               'United States',
        'UK':                'United Kingdom',
    }
    df['full_name'] = df['full_name'].replace(override)
    # 4) 이모지 포함 display_name 생성
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

# 주요 국가 리스트 (display_name)
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

# 전체 국가 목록, 주요 국가를 맨 위로 정렬
all_countries = sorted(df['display_name'].unique())
# 주요 국가가 존재하는 순서대로 뽑아서, 나머지 국가 뒤에 붙이기
others = [c for c in all_countries if c not in major]
options = major + others

st.sidebar.markdown("### 🌍 비교할 국가 선택")
selected = st.sidebar.multiselect(
    "최소 2개 이상의 국가를 선택하세요",
    options=options,
    default=major  # 기본으로 주요 국가 모두 선택
)

if not selected:
    st.sidebar.warning("하나 이상의 국가를 선택해야 그래프를 표시합니다.")
    st.stop()

# 필터링 (연도 ≤ 2050)
df_sel = df[
    (df['display_name'].isin(selected)) &
    (df['year'] <= 2050)
]

# GDP 그래프 (여러 국가 비교)
fig_gdp = px.line(
    df_sel, x='year', y='gdp_pcap', color='display_name',
    labels={'gdp_pcap':'1인당 GDP (USD)', 'year':'연도', 'display_name':'국가'},
    title="1인당 GDP 전망 비교"
)
# 기대수명 그래프
fig_lex = px.line(
    df_sel, x='year', y='lex', color='display_name',
    labels={'lex':'기대수명 (년)', 'year':'연도', 'display_name':'국가'},
    title="기대수명 전망 비교"
)

st.plotly_chart(fig_gdp, use_container_width=True)
st.plotly_chart(fig_lex, use_container_width=True)

# 부가 설명
with st.expander("🔍 사용 설명서"):
    st.write(
        "- 사이드바에서 비교하고 싶은 국가를 여러 개 선택하세요.\n"
        "- 주요 11개 국가는 기본으로 선택되어 있고, 나머지 국가도 스크롤해 선택할 수 있습니다.\n"
        "- 최대 1800~2050년 데이터를 한눈에 비교할 수 있습니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 선택한 국가들 간의 경제·보건 지표 차이는 무엇이 원인일까요?\n"
        "2. 특정 국가 그룹(예: 선진국 vs 개도국) 패턴을 비교해 보세요."
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 그룹별(대륙, 소득 수준) 시나리오 분석 실습\n"
        "- 정책 개입 모델링(고성장/저성장) 비교"
    )
