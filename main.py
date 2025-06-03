import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="📊 데이터 탐험!", layout="wide")
st.title("📁 데이터 파일을 업로드하면 자동으로 분석해줄게요!")

uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 올려보세요", type=["csv", "xlsx"])

if uploaded_file:
    # 파일 읽기
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 📌 데이터 속성 기본 설명
    with st.expander("🧾 데이터 속성 이해 가이드", expanded=True):
        st.markdown("""
**1. 속성 종류**

- **범주형(Categorical)**: 값이 정해진 그룹에 속하는 경우 (예: 성별, 등급)
- **수치형(Numerical)**: 수의 크기나 비율을 비교할 수 있는 값 (예: 나이, 요금)
- **문자형(Textual)**: 이름, 설명 등 자유로운 텍스트
- **날짜형(DateTime)**: 시간 또는 날짜 정보 (예: 가입일, 주문일)

**2. 분석에 자주 사용하는 속성들**

- 📈 **수치형**: 분포, 평균, 중앙값, 이상치, 상관관계 분석에 사용
- 🧩 **범주형**: 그룹별 비교 분석에 적합, 막대그래프 등 시각화 활용
- 🧪 **혼합형**: 예를 들어 날짜별 매출, 범주별 평균 등 교차 분석에 활용
""")

    # 데이터 요약
    st.subheader("🧾 데이터 구조 요약")
    st.markdown(f"- 데이터 행 수: **{df.shape[0]}**개")
    st.markdown(f"- 데이터 열 수: **{df.shape[1]}**개")
    st.markdown(f"- 컬럼 목록: {', '.join(df.columns)}")
    st.markdown(f"- 결측치가 있는 열: {', '.join(df.columns[df.isnull().any()]) or '없음'}")

    # 데이터 타입
    st.write("📌 각 열의 데이터 타입")
    st.dataframe(df.dtypes.rename("Data Type"))

    # 통계 요약
    st.subheader("📈 기본 통계 요약")
    st.dataframe(df.describe())

    # 상관관계 분석
    st.subheader("📌 주요 수치형 열 간의 상관관계")
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu', zmin=-1, zmax=1,
                             title="📊 상관관계 히트맵")
        st.plotly_chart(fig_corr, use_container_width=True)

        # 가장 상관 높은 변수쌍 분석
        high_corr = corr.where(corr < 1).abs().unstack().sort_values(ascending=False).dropna()
        if not high_corr.empty:
            var1, var2 = high_corr.idxmax()
            st.subheader(f"🔍 가장 강한 상관관계: {var1} vs {var2}")
            fig_scatter = px.scatter(df, x=var1, y=var2, title=f"{var1} vs {var2} 관계 시각화")
            st.plotly_chart(fig_scatter, use_container_width=True)

    # 히스토그램 시각화
    st.subheader("📊 수치형 컬럼별 분포")
    for col in num_cols:
        fig_hist = px.histogram(df, x=col, marginal="box", title=f"{col} 분포와 상자그림")
        st.plotly_chart(fig_hist, use_container_width=True)

    # 인사이트 요약
    st.subheader("💡 자동 인사이트 요약")
    if len(num_cols) >= 2:
        st.info(f"📌 **{var1}**와 **{var2}**는 상관계수가 높습니다. 두 변수 간의 관계에 주목해 보세요.")

    if df.isnull().sum().sum() > 0:
        st.warning("⚠️ 결측치가 있는 데이터가 있습니다. 분석 전에 처리하는 것이 좋습니다.")

else:
    st.info("왼쪽에서 파일을 업로드해 주세요.")
