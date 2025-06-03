import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 운영체제에 따라 한글 폰트 설정
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')  # 윈도우 기본 한글 폰트

# 마이너스 기호 깨짐 방지
matplotlib.rcParams['axes.unicode_minus'] = False
# 페이지 세팅
st.set_page_config(page_title="🚢 타이타닉 생존자 분석", layout="wide")

st.title("🚢 타이타닉 생존자 데이터 분석")

# GitHub RAW CSV URL
url = "https://raw.githubusercontent.com/comtlucia/aidataproject/main/titanic.csv"

# 데이터 불러오기
try:
    df = pd.read_csv(url)
    st.success("✅ 파일 불러오기 성공!")
except Exception as e:
    st.error(f"❌ 데이터 불러오기 실패: {e}")
    st.stop()

# 📋 데이터 미리보기
st.subheader("📋 데이터 미리보기")
st.dataframe(df.head())

# 🧾 기본 통계 요약
st.subheader("📈 기본 통계 요약")
num_cols = df.select_dtypes(include='number').columns
st.dataframe(df[num_cols].describe())

# 📊 생존자 수 시각화
st.subheader("📊 전체 생존자 분포")
fig1, ax1 = plt.subplots(figsize=(4,3))
sns.countplot(data=df, x="Survived", ax=ax1)
ax1.set_xticklabels(['사망(0)', '생존(1)'])
st.pyplot(fig1)

# 👥 성별 생존율
st.subheader("👥 성별에 따른 생존율")
if 'Sex' in df.columns:
    gender_surv = df.groupby("Sex")["Survived"].mean().reset_index()
    st.dataframe(gender_surv)

    fig2, ax2 = plt.subplots(figsize=(4,3))
    sns.barplot(data=gender_surv, x="Sex", y="Survived", ax=ax2)
    ax2.set_title("성별 생존율")
    st.pyplot(fig2)

# 🛏️ 객실 등급별 생존율
if 'Pclass' in df.columns:
    st.subheader("🛏️ 객실 등급에 따른 생존율")
    class_surv = df.groupby("Pclass")["Survived"].mean().reset_index()

    fig3, ax3 = plt.subplots(figsize=(4,3))
    sns.barplot(data=class_surv, x="Pclass", y="Survived", ax=ax3)
    ax3.set_title("객실 등급별 생존율")
    st.pyplot(fig3)

# 🎂 나이 분포
if 'Age' in df.columns:
    st.subheader("🎂 나이 분포")
    fig4, ax4 = plt.subplots(figsize=(6,3))
    sns.histplot(df["Age"].dropna(), kde=True, bins=30, ax=ax4)
    st.pyplot(fig4)

# 📌 상관관계 히트맵
st.subheader("📌 숫자형 변수 간 상관관계")
corr = df[num_cols].corr()
fig5, ax5 = plt.subplots(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax5)
st.pyplot(fig5)

# 💡 인사이트 요약 카드
st.subheader("💡 데이터 인사이트 요약")

# 성별 생존율 비교
if 'Sex' in df.columns:
    female_rate = df[df["Sex"] == "female"]["Survived"].mean()
    male_rate = df[df["Sex"] == "male"]["Survived"].mean()
    st.info(f"✅ 여성 생존율: **{female_rate:.2%}**, 남성 생존율: **{male_rate:.2%}** → **여성이 월등히 높음**")

# 객실 등급 생존율
if 'Pclass' in df.columns:
    class_mean = df.groupby("Pclass")["Survived"].mean()
    st.info(f"✅ 객실 등급별 생존율:\n{class_mean.to_string()}\n→ **1등석 승객이 생존율이 가장 높음**")

# 상관관계 분석
corr_pairs = corr.where(corr < 1).abs().unstack().dropna()
if not corr_pairs.empty:
    top_pair = corr_pairs.idxmax()
    value = corr_pairs.max()
    st.info(f"📌 가장 강한 상관관계: **{top_pair[0]} ↔ {top_pair[1]}** → 상관계수 **{value:.2f}**")

st.markdown("---")
st.caption("📊 데이터 기반 사고력 향상을 위한 타이타닉 생존자 분석 앱 by Lucia 👩‍🏫")
