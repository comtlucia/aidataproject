import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🧭 타이타닉 데이터 분석", layout="wide")
st.title("🚢 타이타닉 데이터 탐험")

uploaded_file = st.file_uploader("📁 CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

if uploaded_file:
    # 데이터 불러오기
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("🧾 기본 정보 요약")
    st.markdown(f"- 전체 행 수: **{df.shape[0]}개**")
    st.markdown(f"- 전체 열 수: **{df.shape[1]}개**")
    st.markdown(f"- 컬럼 목록: {', '.join(df.columns)}")
    missing = df.columns[df.isnull().any()]
    st.markdown(f"- 결측치가 있는 열: {', '.join(missing) if len(missing) > 0 else '없음'}")

    # 숫자형 데이터 선택
    num_cols = df.select_dtypes(include="number").columns
    st.subheader("📈 기본 통계 요약")
    st.dataframe(df[num_cols].describe())

    # 히스토그램
    st.subheader("📊 히스토그램으로 살펴보는 변수 분포")
    for col in num_cols:
        st.markdown(f"**{col}**")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        st.pyplot(fig)

    # 상자그림
    st.subheader("📦 이상치 탐색 (상자그림)")
    for col in num_cols:
        fig, ax = plt.subplots(figsize=(6, 1.5))
        sns.boxplot(x=df[col].dropna(), ax=ax)
        st.pyplot(fig)

    # 상관관계 분석
    st.subheader("📌 변수 간 상관관계 히트맵")
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    # 상관관계 인사이트 분석
    st.subheader("💡 데이터 인사이트 카드")

    # 1. 가장 강한 상관 변수쌍
    corr_pairs = corr.where(corr < 1).abs().unstack().dropna()
    if not corr_pairs.empty:
        top_pair = corr_pairs.idxmax()
        top_value = corr_pairs.max()
        st.success(f"🔍 **'{top_pair[0]}'** 와 **'{top_pair[1]}'** 는 상관계수 **{top_value:.2f}** 로 매우 강한 관계입니다. 중복 변수일 가능성이 있습니다.")

    # 2. Age vs Fare
    if "Age" in num_cols and "Fare" in num_cols:
        age_fare = corr.loc["Age", "Fare"]
        st.info(f"👥 `Age` 와 `Fare` 의 상관관계는 **{age_fare:.2f}** 입니다. 나이가 많다고 반드시 비싼 티켓을 샀다고 보기는 어렵습니다.")

    # 3. SibSp vs Parch
    if "SibSp" in num_cols and "Parch" in num_cols:
        sib_parch = corr.loc["SibSp", "Parch"]
        st.info(f"👨‍👩‍👧‍👦 `SibSp` 와 `Parch` 의 상관관계는 **{sib_parch:.2f}** 입니다. 가족 단위로 탑승한 경향을 나타냅니다.")

    st.markdown("---")
    st.caption("ⓒ 고등학생을 위한 탐색적 데이터 분석 연습. 파일만 올려도 자동 분석!")
else:
    st.info("왼쪽에서 CSV 또는 Excel 파일을 업로드해 주세요!")
