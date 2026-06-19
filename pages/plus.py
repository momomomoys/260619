import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="글로벌 시가총액 TOP10 주식 대시보드",
    page_icon="📈",
    layout="wide"
)

st.title("🌎 글로벌 시가총액 TOP10 주식 대시보드")
st.markdown("최근 1년간 주가 변화 비교")

# 글로벌 시가총액 TOP10 (2026 기준 대표 기업)
stocks = {
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Saudi Aramco": "2222.SR",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Berkshire Hathaway": "BRK-B"
}

# 종목 선택
selected = st.multiselect(
    "비교할 기업 선택",
    list(stocks.keys()),
    default=list(stocks.keys())[:5]
)

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

@st.cache_data
def load_data(tickers):
    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )
    return data

if selected:

    ticker_list = [stocks[s] for s in selected]

    with st.spinner("데이터 불러오는 중..."):
        data = load_data(ticker_list)

    close_df = data["Close"]

    if len(ticker_list) == 1:
        close_df = close_df.to_frame()

    # 정규화
    normalized = close_df / close_df.iloc[0] * 100

    fig = px.line(
        normalized,
        x=normalized.index,
        y=normalized.columns,
        title="최근 1년 수익률 비교 (시작값=100)"
    )

    fig.update_layout(
        height=650,
        xaxis_title="날짜",
        yaxis_title="상대 주가",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 성과 요약")

    summary = []

    for col in normalized.columns:
        start = normalized[col].iloc[0]
        end = normalized[col].iloc[-1]
        change = ((end - start) / start) * 100

        summary.append(
            {
                "Ticker": col,
                "1년 수익률 (%)": round(change, 2)
            }
        )

    summary_df = pd.DataFrame(summary)
    summary_df = summary_df.sort_values(
        "1년 수익률 (%)",
        ascending=False
    )

    st.dataframe(summary_df, use_container_width=True)

st.markdown("---")

marketcap_df = pd.DataFrame({
    "기업": [
        "Microsoft",
        "NVIDIA",
        "Apple",
        "Amazon",
        "Alphabet",
        "Meta",
        "Saudi Aramco",
        "Broadcom",
        "TSMC",
        "Berkshire Hathaway"
    ],
    "티커": [
        "MSFT",
        "NVDA",
        "AAPL",
        "AMZN",
        "GOOGL",
        "META",
        "2222.SR",
        "AVGO",
        "TSM",
        "BRK-B"
    ]
})

st.subheader("🏆 글로벌 시가총액 TOP10")
st.dataframe(marketcap_df, use_container_width=True)
