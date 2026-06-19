import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from io import BytesIO

st.set_page_config(
    page_title="서울 기후변화 탐험대",
    page_icon="🌏",
    layout="wide"
)

# ==========================
# 데이터 로드
# ==========================
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20260619190504.csv")

    # 컬럼명 정리
    df.columns = [c.strip() for c in df.columns]

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df


df = load_data()

# ==========================
# 제목
# ==========================

st.title("🌏 서울 기후변화 탐험대")
st.markdown("### 1907 ~ 2026 서울 기온 데이터 분석")

# ==========================
# 사이드바
# ==========================

st.sidebar.header("🔍 데이터 필터")

start_year = st.sidebar.slider(
    "시작 연도",
    int(df["연도"].min()),
    int(df["연도"].max()),
    int(df["연도"].min())
)

end_year = st.sidebar.slider(
    "종료 연도",
    int(df["연도"].min()),
    int(df["연도"].max()),
    int(df["연도"].max())
)

month = st.sidebar.selectbox(
    "월 선택",
    ["전체"] + list(range(1, 13))
)

filtered = df[
    (df["연도"] >= start_year) &
    (df["연도"] <= end_year)
]

if month != "전체":
    filtered = filtered[filtered["월"] == month]

# ==========================
# 기온 상승량 계산
# ==========================

old_period = df[(df["연도"] >= 1907) & (df["연도"] <= 1930)]
recent_period = df[(df["연도"] >= 1997)]

old_avg = old_period["평균기온(℃)"].mean()
recent_avg = recent_period["평균기온(℃)"].mean()

increase = recent_avg - old_avg

# ==========================
# 상단 카드
# ==========================

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
    "기온 상승",
    f"{increase:.2f}℃"
)

# ==========================
# 연평균 기온
# ==========================

st.subheader("📈 연평균 기온 변화")

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
    markers=True
)

# 추세선
x = annual["연도"]
y = annual["평균기온(℃)"]

coef = np.polyfit(x, y, 1)
trend = np.poly1d(coef)

fig.add_trace(
    go.Scatter(
        x=x,
        y=trend(x),
        mode="lines",
        name="추세선"
    )
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# 월별 평균기온
# ==========================

st.subheader("🌡️ 월별 평균 기온")

monthly = (
    filtered
    .groupby("월")["평균기온(℃)"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    monthly,
    x="월",
    y="평균기온(℃)"
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================
# 히트맵
# ==========================

st.subheader("🔥 연도 × 월 평균기온 히트맵")

heat = (
    filtered
    .pivot_table(
        values="평균기온(℃)",
        index="연도",
        columns="월",
        aggfunc="mean"
    )
)

fig3 = px.imshow(
    heat,
    aspect="auto",
    labels=dict(color="기온")
)

st.plotly_chart(fig3, use_container_width=True)

# ==========================
# 최고 최저 기록
# ==========================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🔥 역대 최고기온 TOP10")

    top_hot = (
        df.nlargest(10, "최고기온(℃)")
        [["날짜", "최고기온(℃)"]]
    )

    st.dataframe(top_hot, use_container_width=True)

with col2:

    st.subheader("❄️ 역대 최저기온 TOP10")

    top_cold = (
        df.nsmallest(10, "최저기온(℃)")
        [["날짜", "최저기온(℃)"]]
    )

    st.dataframe(top_cold, use_container_width=True)

# ==========================
# 생일 기온 조회
# ==========================

st.subheader("🎂 내가 태어난 날 기온")

birthday = st.date_input("생일 선택")

result = df[df["날짜"] == pd.Timestamp(birthday)]

if len(result) > 0:

    row = result.iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "평균기온",
        f"{row['평균기온(℃)']:.1f}℃"
    )

    c2.metric(
        "최저기온",
        f"{row['최저기온(℃)']:.1f}℃"
    )

    c3.metric(
        "최고기온",
        f"{row['최고기온(℃)']:.1f}℃"
    )

else:
    st.info("해당 날짜 데이터가 없습니다.")

# ==========================
# 미래 예측
# ==========================

st.subheader("🔮 미래 서울 기온 예측")

annual_full = (
    df.groupby("연도")["평균기온(℃)"]
    .mean()
    .reset_index()
)

X = annual_full[["연도"]]
y = annual_full["평균기온(℃)"]

model = LinearRegression()
model.fit(X, y)

future_years = pd.DataFrame({
    "연도": [2030, 2040, 2050]
})

future_years["예측기온"] = model.predict(future_years)

c1, c2, c3 = st.columns(3)

c1.metric(
    "2030년",
    f"{future_years.iloc[0]['예측기온']:.2f}℃"
)

c2.metric(
    "2040년",
    f"{future_years.iloc[1]['예측기온']:.2f}℃"
)

c3.metric(
    "2050년",
    f"{future_years.iloc[2]['예측기온']:.2f}℃"
)

# ==========================
# 다운로드
# ==========================

st.subheader("⬇️ 데이터 다운로드")

csv = filtered.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="CSV 다운로드",
    data=csv,
    file_name="seoul_climate_filtered.csv",
    mime="text/csv"
)
