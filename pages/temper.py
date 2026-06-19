
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="서울 기후변화 탐험대",
    page_icon="🌏",
    layout="wide"
)

@st.cache_data
def load_data():

    df = pd.read_csv("ta_20260619190504.csv")

    # 컬럼명 정리
    df.columns = df.columns.str.strip()

    # 날짜 앞 탭/공백 제거
    df["날짜"] = (
        df["날짜"]
        .astype(str)
        .str.replace("\t", "", regex=False)
        .str.strip()
    )

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 날짜 변환 실패 제거
    df = df.dropna(subset=["날짜"])

    # 기온 데이터 숫자 변환
    temp_cols = [
        "평균기온(℃)",
        "최저기온(℃)",
        "최고기온(℃)"
    ]

    for col in temp_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # 파생 변수
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df


df = load_data()

st.title("🌏 서울 기후변화 탐험대")

# --------------------
# 사이드바
# --------------------

st.sidebar.header("데이터 선택")

start_year = st.sidebar.slider(
    "시작 연도",
    int(df["연도"].min()),
    int(df["연도"].max()),
    1907
)

end_year = st.sidebar.slider(
    "종료 연도",
    int(df["연도"].min()),
    int(df["연도"].max()),
    2026
)

filtered = df[
    (df["연도"] >= start_year) &
    (df["연도"] <= end_year)
]

# --------------------
# KPI
# --------------------

old_avg = df[
    (df["연도"] >= 1907) &
    (df["연도"] <= 1930)
]["평균기온(℃)"].mean()

recent_avg = df[
    df["연도"] >= 1997
]["평균기온(℃)"].mean()

increase = recent_avg - old_avg

c1, c2, c3 = st.columns(3)

c1.metric(
    "1907~1930 평균",
    f"{old_avg:.2f}℃"
)

c2.metric(
    "최근 30년 평균",
    f"{recent_avg:.2f}℃"
)

c3.metric(
    "상승량",
    f"{increase:.2f}℃"
)

# --------------------
# 연평균기온
# --------------------

annual = (
    filtered
    .groupby("연도")["평균기온(℃)"]
    .mean()
    .reset_index()
)

fig = px.line(
    annual,
    x="연도",
    y="평균기온(℃)",
    title="연평균기온 변화"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------
# 월별 평균기온
# --------------------

monthly = (
    filtered
    .groupby("월")["평균기온(℃)"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    monthly,
    x="월",
    y="평균기온(℃)",
    title="월별 평균기온"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------
# 히트맵
# --------------------

heat = filtered.pivot_table(
    values="평균기온(℃)",
    index="연도",
    columns="월",
    aggfunc="mean"
)

fig3 = px.imshow(
    heat,
    aspect="auto",
    title="연도 × 월 평균기온"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# --------------------
# 최고기온 TOP10
# --------------------

st.subheader("🔥 역대 최고기온 TOP10")

top_hot = (
    df.nlargest(
        10,
        "최고기온(℃)"
    )[["날짜", "최고기온(℃)"]]
)

st.dataframe(
    top_hot,
    use_container_width=True
)

# --------------------
# 최저기온 TOP10
# --------------------

st.subheader("❄️ 역대 최저기온 TOP10")

top_cold = (
    df.nsmallest(
        10,
        "최저기온(℃)"
    )[["날짜", "최저기온(℃)"]]
)

st.dataframe(
    top_cold,
    use_container_width=True
)

# --------------------
# 미래 예측
# --------------------

st.subheader("🔮 미래 기온 예측")

coef = np.polyfit(
    annual["연도"],
    annual["평균기온(℃)"],
    1
)

future = [2030, 2040, 2050]

cols = st.columns(3)

for i, year in enumerate(future):

    pred = coef[0] * year + coef[1]

    cols[i].metric(
        f"{year}년",
        f"{pred:.2f}℃"
    )

# --------------------
# 다운로드
# --------------------

csv = filtered.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    "CSV 다운로드",
    csv,
    "seoul_climate.csv",
    "text/csv"
)
