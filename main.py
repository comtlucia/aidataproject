import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="📊 데이터 탐험!", layout="wide")
st.title("📁 데이터 파일을 업로드하면 자동으로 분석해줄게요!")

uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 올려보세요", type=["csv", "xlsx"])

if uploaded_file:
    # 데이터 불러오기
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # ---------------- 데이터 요약 ---------------- #
    st.subheader("🧾 데이터 구조 요약")
    st.markdown(f"- 데이터 행 수: **{df.shape[0]}**개")
    st.markdown(f"- 데이터 열 수: **{df.shape[1]}**개")
    st.markdown(f"- 컬럼 목록: {', '.join(df.columns)}")
    st.markdown(f"- 결측치 있는 열: {', '.join(df.columns[df.isnull().any()]) or '없음'}")

    st.write("📌 각 열의 데이터 타입")
    st.dataframe(df.dtypes.rename("Data Type"))

    st.subheader("📈 기본 통계 요약")
    st.dataframe(df.describe().transpose(), use_container_width=True)

    # ---------------- 수치형 컬럼 추출 ---------------- #
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) == 0:
        st.warning("수치형 컬럼이 없어 분석할 수 없습니다.")
        st.stop()

    # ---------------- 상관관계 분석 ---------------- #
    st.subheader("📌 상관관계 히트맵")
    corr = df[num_cols].corr().round(2)
    text = np.array([[f"{val:.2f}" for val in row] for row in corr.values])

    fig_corr = px.imshow(
        corr,
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1,
        labels=dict(color="상관계수"),
        x=corr.columns,
        y=corr.index,
        title="수치형 변수 간 상관관계 히트맵"
    )
    fig_corr.update_traces(text=text, texttemplate="%{text}", textfont_size=14)
    fig_corr.update_layout(height=700, title_font_size=22)
    st.plotly_chart(fig_corr, use_container_width=True)

    # ---------------- 중요한 속성 분석 ---------------- #
    st.subheader("🔍 상관관계 높은 속성 분석")

    # 상관계수 높은 변수쌍 추출
    high_corr = corr.where(corr < 1).abs().unstack().sort_values(ascending=False).dropna()
    top_pairs = high_corr[~high_corr.index.duplicated()].head(2)

    for (var1, var2), value in top_pairs.items():
        st.markdown(f"### 📈 **{var1} vs {var2}** (상관계수: {value:.2f})")
        fig = px.scatter(df, x=var1, y=var2, trendline="ols", title=f"{var1} vs {var2} 관계")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- 기본 시각화 ---------------- #
    st.subheader("📊 수치형 변수 히스토그램")
    for col in num_cols:
        fig = px.histogram(df, x=col, nbins=30, marginal="box", title=f"{col}의 분포")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📦 수치형 변수 상자그림 (이상치 확인)")
    for col in num_cols:
        fig = px.box(df, x=col, title=f"{col}의 이상치 분포")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- 인사이트 카드 ---------------- #
    st.subheader("💡 데이터에서 알 수 있는 인사이트")

    mean_col = df[num_cols].mean().idxmax()
    st.success(f"✅ **{mean_col}**은(는) 평균값이 가장 높습니다. 중요한 기준이 될 수 있어요.")

    if not top_pairs.empty:
        var1, var2 = top_pairs.index[0]
        st.info(f"🔗 **{var1}**와 **{var2}**은(는) 가장 강한 상관관계를 가집니다. 함께 분석하면 의미 있는 인사이트를 얻을 수 있어요.")

    if df.isnull().sum().sum() > 0:
        st.warning("⚠️ 결측치가 있습니다. 분석 전 처리하는 것이 좋습니다.")

else:
    st.info("왼쪽에서 파일을 업로드해 주세요.")
