import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SDG 8: 2050년까지 GDP · 기대수명 전망")
st.write(
    "기존 데이터를 바탕으로 선택한 국가의 2050년까지 1인당 GDP와 기대수명 변화를 시각화합니다."
)
st.markdown("---")

@st.cache_data
def load_data():
    # 1) 주요 시계열 데이터 로드
    df_main = pd.read_csv('data/merged_gapminder.csv')
    
    # 2) 엔티티 매핑 파일 로드 (ISO → 풀 네임)
    df_geo = pd.read_csv('data/ddf--entities--geo--country.csv', usecols=['country','name'])
    df_geo = df_geo.rename(columns={'name':'full_name'})
    
    # 3) 합치기
    df = df_main.merge(df_geo, on='country', how='left')
    
    # 4) 일부 이름 override
    override = {
        'South Korea':       'Republic of Korea',
        'USA':               'United States',
        'UK':                'United Kingdom',
    }
    df['full_name'] = df['full_name'].replace(override)
    
    # 5) 주요 국가에 국기 이모지 추가
    flags = {
        'United States':    '🇺🇸',
        'China':            '🇨🇳',
        'India':            '🇮🇳',
        'Japan':            '🇯🇵',
        'Germany':          '🇩🇪',
        'United Kingdom':   '🇬🇧',
        'Republic of Korea':'🇰🇷',
        'France':           '🇫🇷',
        'Brazil':           '🇧🇷',
        'Canada':           '🇨🇦',
        'Australia':        '🇦🇺'
    }
    df['display_name'] = df['full_name'].apply(
        lambda n: f"{flags[n]} {n}" if n in flags else n
    )
    
    return df

df = load_data()

# 6) 사이드바: 모든 국가 풀 네임으로 선택 가능
countries = sorted(df['display_name'].unique())
selected = st.sidebar.selectbox("🌍 국가를 선택하세요", countries)

# 7) 선택된 국가·2050년 이하 필터
country_df = df[
    (df['display_name'] == selected) &
    (df['year'] <= 2050)
]

# 8) 그래프
fig_gdp = px.line(
    country_df, x='year', y='gdp_pcap',
    labels={'gdp_pcap':'1인당 GDP (USD)', 'year':'연도'},
    title=f"{selected}의 1인당 GDP 전망"
)
fig_lex = px.line(
    country_df, x='year', y='lex',
    labels={'lex':'기대수명 (년)', 'year':'연도'},
    title=f"{selected}의 기대수명 전망"
)

st.plotly_chart(fig_gdp, use_container_width=True)
st.plotly_chart(fig_lex, use_container_width=True)

# 9) 설명 확장
with st.expander("🔍 사용 설명서"):
    st.write(
        "- 사이드바에서 원하는 국가를 검색 또는 스크롤하여 선택하세요.\n"
        "- 선택한 국가의 1800~2050년 범위 데이터를 자동으로 보여줍니다."
    )

with st.expander("💡 학생 토론 질문"):
    st.markdown(
        "1. 선택한 국가의 경제·보건 지표 변화를 어떻게 해석할 수 있을까?\n"
        "2. SDG 달성을 위해 각국이 취할 수 있는 정책은 무엇일까?"
    )

with st.expander("📚 교육적 함의 및 확장 활동"):
    st.write(
        "- 데이터 기반 예측의 한계와 가능성 논의\n"
        "- 다양한 시나리오(고성장·저성장 등) 모델링 실습"
    )
