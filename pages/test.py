import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🚢 타이타닉 생존자 분석 대시보드")

# 데이터 불러오기
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/comtlucia/aidataproject/main/titanic.csv"
    return pd.read_csv(url)

df = load_data()

# 기본 정보 표시
st.markdown(f"""
- 전체 승객 수: **{len(df)}명**
- 분석 기준 컬럼: `Sex`, `Pclass`, `Survived`, `Age`, `Fare`, `SibSp`, `Parch`
""")
# 데이터 요약 출력
st.markdown("## 🧾 데이터 요약 정보")
st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

# 결측치 정보 요약
st.markdown("### 🔍 결측치 현황")
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
if not missing.empty:
    st.dataframe(missing.to_frame("결측치 수"), use_container_width=True)
else:
    st.success("결측치가 없습니다.")

# 성별 생존자 수 시각화
sex_surv = df.groupby(['Sex', 'Survived']).size().reset_index(name='Count')

fig_sex = go.Figure()
for value in sorted(sex_surv["Survived"].unique()):
    data = sex_surv[sex_surv["Survived"] == value]
    fig_sex.add_trace(go.Bar(
        x=data["Sex"],
        y=data["Count"],
        name="생존" if value == 1 else "사망",
        text=data["Count"],
        textposition="outside"
    ))

fig_sex.update_layout(
    title="👨‍👩‍👧‍👦 성별 생존자 수",
    barmode="group",
    height=400,
    xaxis_title="성별",
    yaxis_title="명 수"
)

# 객실 등급별 생존율
class_surv = df.groupby("Pclass")["Survived"].mean().reset_index()
class_surv["Survived"] = (class_surv["Survived"] * 100).round(2)

fig_class = go.Figure(go.Bar(
    x=class_surv["Pclass"].astype(str),
    y=class_surv["Survived"],
    text=class_surv["Survived"].astype(str) + "%",
    textposition="outside",
    marker_color="lightcoral"
))
fig_class.update_layout(
    title="🏨 객실 등급별 생존율",
    height=400,
    xaxis_title="객실 등급",
    yaxis_title="생존율 (%)"
)

# 나이 분포: 생존 vs 사망
df_age = df.dropna(subset=["Age"])
fig_age = go.Figure()
fig_age.add_trace(go.Box(y=df_age[df_age["Survived"] == 1]["Age"], name="생존자", boxpoints="outliers"))
fig_age.add_trace(go.Box(y=df_age[df_age["Survived"] == 0]["Age"], name="사망자", boxpoints="outliers"))
fig_age.update_layout(
    title="📈 나이에 따른 생존 여부 분포",
    yaxis_title="나이",
    height=400
)

# 요금 분포: 생존 vs 사망
df_fare = df[df["Fare"] < 200]  # 이상치 제거
fig_fare = go.Figure()
fig_fare.add_trace(go.Box(y=df_fare[df_fare["Survived"] == 1]["Fare"], name="생존자"))
fig_fare.add_trace(go.Box(y=df_fare[df_fare["Survived"] == 0]["Fare"], name="사망자"))
fig_fare.update_layout(
    title="💰 요금(Fare)에 따른 생존 여부 분포 (200 이하)",
    yaxis_title="요금",
    height=400
)

# 레이아웃 배치
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_sex, use_container_width=True)
with col2:
    st.plotly_chart(fig_class, use_container_width=True)

st.plotly_chart(fig_age, use_container_width=True)
st.plotly_chart(fig_fare, use_container_width=True)

# 📌 수치형 변수 간 상관관계 히트맵
st.markdown("## 📊 수치형 변수 간 상관관계 분석")

num_cols = ["Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]
df_corr = df[num_cols].dropna().corr()

fig_corr = px.imshow(
    df_corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="📌 상관관계 히트맵 (Survived 중심)"
)
fig_corr.update_layout(height=500)

st.plotly_chart(fig_corr, use_container_width=True)

# 인사이트 요약
st.markdown("## 🧠 분석 인사이트 요약")
st.info("""
- 👩 여성의 생존율이 남성보다 매우 높았습니다.
- 🏨 1등급 객실 승객의 생존율이 가장 높고, 3등급 객실의 생존율은 낮았습니다.
- 📊 나이 분포에서 어린 승객의 생존 가능성이 다소 높게 나타났습니다.
- 💰 요금이 높을수록 생존율도 높아지는 경향이 있었습니다.
- 🔗 상관관계 분석 결과, `Pclass`와 `Fare`는 강한 음의 상관, `SibSp`와 `Parch`는 강한 양의 상관을 보였습니다.
""")
