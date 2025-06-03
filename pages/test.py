import streamlit as st
import pandas as pd

st.title("🚢 GitHub에서 타이타닉 데이터 불러오기")

# RAW GitHub 파일 URL
url = "https://raw.githubusercontent.com/comtlucia/aidataproject/main/titanic.csv"

# 데이터 읽기
try:
    df = pd.read_csv(url)
    st.success("✅ 파일 불러오기 성공!")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ 오류 발생: {e}")
