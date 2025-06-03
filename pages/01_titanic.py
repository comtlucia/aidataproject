import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🧭 데이터 분석 앱", layout="wide")
st.title("📊 파일만 올려도 분석이 되는 Streamlit 앱")

uploaded_file = st.file_uploader("파일을 업로드하세요 (CSV 또는 Excel)", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📋 데이터 기본 요약")
    st.markdown(f"- 행 수: **{df.shape[0]}개**, 열 수: **{df.shape[1]}개**")
    st.markdown(f"- 컬럼: `{', '.join(df.columns[:10])}` ...")
    null_cols = df.columns[df.isnull().any()]
    st.markdown(f"- 결측치 있는 열: `{', '.join(null_cols) if len(null_cols) > 0 else '없음'}`")

    num_cols = df.select_dtypes(include="number").columns

    st.subheader("📈 숫자형 컬럼 통계 요약")
    st.dataframe(df[num_cols].describe())

    st.subheader("📊 히스토그램 (데이터 분포)")
    for col in num_cols:
        st.markdown(f"**🔹 {col}**")
        fig, ax = plt.subplots(figsize=(4, 2.5))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        st.pyplot(fig)

    st.subheader("📦 이상치 탐색 (상자그림)")
    for col in num_cols:
        fig, ax = plt.subplots(figsize=(4, 1.5))
        sns.boxplot(x=df[col].dropna(), ax=ax)
        st.pyplot(fig)

    st.subheader("📌 상관관계 히트맵")
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(4, 3))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.subheader("💡 데이터 분석 인사이트")

    # 주요 상관관계 도출
    corr_pairs = corr.where(corr < 1).abs().unstack().dropna()
    if not corr_pairs.empty:
        top_pair = corr_pairs.idxmax()
        top_value = corr_pairs.max()
        st.success(f"""
        🔍 **'{top_pair[0]}'**와 **'{top_pair[1]}'** 간 상관계수는 **{top_value:.2f}**로 매우 강한 상관관계를 보입니다.  
        → 두 변수는 서로 강하게 연결되어 있으며, **유사한 의미**를 지니거나 **동일한 원인의 영향을 받을 수 있습니다.**
        """)

    # Age vs Fare
    if "Age" in num_cols and "Fare" in num_cols:
        af_corr = corr.loc["Age", "Fare"]
        st.info(f"""
        👵 **Age(나이)** 와 **Fare(운임)** 간 상관계수는 **{af_corr:.2f}**입니다.  
        → 즉, **나이가 많다고 반드시 비싼 요금을 지불하진 않았습니다.** 연령과 지불 능력 간 직접적 연관성은 낮습니다.
        """)

    # SibSp vs Parch
    if "SibSp" in num_cols and "Parch" in num_cols:
        sp_corr = corr.loc["SibSp", "Parch"]
        st.info(f"""
        👨‍👩‍👧‍👦 **SibSp(형제/배우자 수)** 와 **Parch(부모/자녀 수)** 간 상관계수는 **{sp_corr:.2f}**입니다.  
        → 이는 **가족 단위로 함께 탑승한 승객**이 많았다는 의미일 수 있습니다.
        """)

    # 전체 인사이트 요약
    st.markdown("""
    ---  
    📌 **데이터 속 변수들 간의 연결성**은 단순한 숫자보다 더 많은 이야기를 담고 있습니다.  
    학생들은 어떤 변수가 결과(예: 생존 여부, 성적 등)에 영향을 미칠 수 있을지 **가설을 세우고 직접 검증하는 활동**으로 확장할 수 있습니다.
    """)
else:
    st.info("CSV 또는 Excel 파일을 업로드해 주세요!")
