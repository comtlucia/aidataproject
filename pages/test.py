import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import platform
import io

st.title("🚢 GitHub에서 타이타닉 데이터 불러오기")

# ✅ 한글 폰트 설정 (Windows 환경 기준)
if platform.system() == 'Windows':
    matplotlib.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    matplotlib.rcParams['font.family'] = 'AppleGothic'
else:
    matplotlib.rcParams['font.family'] = 'NanumGothic'

matplotlib.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 불러오기 (GitHub의 RAW CSV)
url = "https://raw.githubusercontent.com/comtlucia/aidataproject/main/titanic.csv"
df = pd.read_csv(url)

st.title("🚢 타이타닉 데이터 시각화")

# ✅ 성별 생존자 수 그래프 생성
fig1, ax1 = plt.subplots(figsize=(3, 2))
sns.countplot(data=df, x="Sex", hue="Survived", ax=ax1)
ax1.set_title("성별 생존자 수")
ax1.set_xlabel("성별")
ax1.set_ylabel("명 수")
buf1 = io.BytesIO()
fig1.savefig(buf1, format="png", bbox_inches="tight", dpi=100)
buf1.seek(0)

# ✅ 객실 등급별 생존율 그래프 생성
class_surv = df.groupby("Pclass")["Survived"].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(3, 2))
sns.barplot(data=class_surv, x="Pclass", y="Survived", ax=ax2)
ax2.set_title("객실 등급별 생존율")
ax2.set_xlabel("등급")
ax2.set_ylabel("생존율")
buf2 = io.BytesIO()
fig2.savefig(buf2, format="png", bbox_inches="tight", dpi=100)
buf2.seek(0)

# ✅ Streamlit 화면에 나란히 출력
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 성별 생존자 수")
    st.image(buf1)

with col2:
    st.subheader("🏨 객실 등급 생존율")
    st.image(buf2)
