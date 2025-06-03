import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 경고 무시
import warnings
warnings.filterwarnings("ignore")

# 🔗 GitHub에 올린 raw 파일 주소를 아래에 입력
ur = "titanic.csv"
df = pd.read_csv(ur)

# ✅ 1. 기본 정보
print("📌 데이터 기본 정보")
print(df.info())
print("\n📌 통계 요약")
print(df.describe(include="all"))

# ✅ 2. 결측치 분석
print("\n📌 결측치 개수")
print(df.isnull().sum())

# ✅ 3. 생존자 분포
sns.countplot(data=df, x="Survived")
plt.title("생존자 vs 사망자")
plt.xlabel("0 = 사망, 1 = 생존")
plt.ylabel("승객 수")
plt.show()

# ✅ 4. 성별 생존율
sns.barplot(data=df, x="Sex", y="Survived")
plt.title("성별 생존율")
plt.show()

# ✅ 5. 객실 등급 생존율
sns.barplot(data=df, x="Pclass", y="Survived")
plt.title("객실 등급별 생존율")
plt.show()

# ✅ 6. 나이 분포
sns.histplot(df["Age"].dropna(), kde=True, bins=30)
plt.title("나이 분포")
plt.xlabel("나이")
plt.ylabel("승객 수")
plt.show()

# ✅ 7. 상관관계 히트맵
numeric_cols = df.select_dtypes(include="number")
corr = numeric_cols.corr()

plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("숫자형 변수 간 상관관계")
plt.show()

# ✅ 8. 인사이트 요약
print("\n💡 주요 인사이트:")
if "Sex" in df.columns and "Survived" in df.columns:
    female_surv = df[df["Sex"] == "female"]["Survived"].mean()
    male_surv = df[df["Sex"] == "male"]["Survived"].mean()
    print(f"1️⃣ 여성 생존율: {female_surv:.2%}, 남성 생존율: {male_surv:.2%}")
    print("→ 여성의 생존율이 월등히 높습니다.")

if "Pclass" in df.columns:
    class_surv = df.groupby("Pclass")["Survived"].mean()
    print(f"\n2️⃣ 객실 등급별 생존율:\n{class_surv}")
    print("→ 상위 객실일수록 생존율이 높습니다.")

if "Age" in df.columns:
    print(f"\n3️⃣ 평균 나이: {df['Age'].mean():.1f}세")
    print("→ 대부분의 승객은 20~40대입니다.")
