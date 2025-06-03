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

    # 데이터 요약
    st.subheader("🧾 데이터 구조 요약")
    st.markdown(f"- 데이터 행 수: **{df.shape[0]}**개")
    st.markdown(f"- 데이터 열 수: **{df.shape[1]}**개")
    st.markdown(f"- 컬럼 목록: {', '.join(df.columns)}")
    st.markdown(f"- 결측치가 있는 열: {', '.join(df.columns[df.isnull().any()]) or '없음'}")

    st.write("📌 각 열의 데이터 타입")
    st.dataframe(df.dtypes.rename("Data Type"))

    # 통계 요약
    st.subheader("📈 기본 통계 요약")
    st.dataframe(df.describe().transpose(), use_container_width=True)

    # 시각화
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) == 0:
        st.warning("수치형 컬럼이 없어 시각화를 진행할 수 없습니다.")
    else:
        st.subheader("📊 컬럼별 히스토그램")
        for col in num_cols:
            fig = px.histogram(df, x=col, nbins=30, marginal="box", title=f"{col}의 분포")
            st.plotly_chart(fig, use_container_width=True)

        # 상자그림
        st.subheader("📦 이상치 확인 (상자그림)")
        for col in num_cols:
            fig = px.box(df, x=col, title=f"{col}의 이상치 분포")
            st.plotly_chart(fig, use_container_width=True)

        # 상관관계 히트맵
        st.subheader("📌 상관관계 히트맵")
        corr = df[num_cols].corr()
        fig_corr = px.imshow(
            corr,
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            labels=dict(color="상관계수"),
            title="수치형 변수 간 상관관계 히트맵"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

        # 인사이트 카드
        st.subheader("💡 데이터에서 알 수 있는 인사이트")

        # 평균이 가장 높은 항목
        mean_col = df[num_cols].mean().idxmax()
        st.success(f"✅ **{mean_col}**은(는) 평균값이 가장 높습니다. 데이터 분석의 중요한 기준이 될 수 있어요.")

        # 상관계수가 높은 변수쌍
        high_corr = corr.where(corr < 1).abs().unstack().sort_values(ascending=False).dropna()
        if not high_corr.empty:
            top_pair = high_corr.idxmax()
            st.info(f"🔗 **{top_pair[0]}**와 **{top_pair[1]}**은(는) 강한 상관관계를 가지고 있어요.")

        # 결측치
        if df.isnull().sum().sum() > 0:
            st.warning("⚠️ 결측치가 있는 데이터가 있습니다. 분석 전에 처리하는 것이 좋습니다.")

else:
    st.info("왼쪽에서 파일을 업로드해 주세요.")
