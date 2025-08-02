# financial_dashboard.py

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Streamlit config
st.set_page_config(page_title="📊 Financial Dashboard", layout="wide")
st.title(":bar_chart: Financial Data Dashboard")

# Sidebar inputs
st.sidebar.header("Query Parameters")

default_tickers = ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'AMZN', 'META']
ticker = st.sidebar.selectbox("Choose a Stock", default_tickers)
start_date = st.sidebar.date_input("Start Date", value=datetime.today() - timedelta(days=180))
end_date = st.sidebar.date_input("End Date", value=datetime.today())
ma_window = st.sidebar.slider("Moving Average Window", min_value=5, max_value=60, value=20)
rsi_period = st.sidebar.slider("RSI Period", min_value=5, max_value=30, value=14)

# Fetch data
@st.cache_data
def get_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df

def calculate_moving_average(df, window):
    df["MA"] = df["Close"].rolling(window=window).mean()
    return df

def calculate_rsi(df, period=14):
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df["RSI"] = rsi
    return df

def plot_price(df, ticker):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="#00BFFF", width=2),
        fill="tozeroy",
        fillcolor="rgba(0,191,255,0.2)"
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["MA"],
        mode="lines",
        name=f"{ma_window}-Day MA",
        line=dict(color="#FF7F50", dash="dot", width=2)
    ))

    fig.update_layout(
        title=f"{ticker} Price with Moving Average",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        height=500,
        font=dict(size=14),
        hovermode="x unified"
    )

    return fig

def plot_volume(df, ticker):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volume"],
        marker_color="#20c997",
        name="Volume"
    ))

    fig.update_layout(
        title=f"{ticker} Daily Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_dark",
        height=300,
        font=dict(size=14),
        hovermode="x unified"
    )

    return fig

def plot_rsi(df, ticker):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["RSI"],
        mode="lines",
        name="RSI",
        line=dict(color="#FFD700", width=2)
    ))

    fig.add_shape(type="line", x0=df.index.min(), x1=df.index.max(), y0=70, y1=70,
                  line=dict(color="red", width=1, dash="dash"))
    fig.add_shape(type="line", x0=df.index.min(), x1=df.index.max(), y0=30, y1=30,
                  line=dict(color="green", width=1, dash="dash"))

    fig.update_layout(
        title=f"{ticker} RSI (Relative Strength Index)",
        xaxis_title="Date",
        yaxis_title="RSI",
        yaxis_range=[0, 100],
        template="plotly_dark",
        height=300,
        font=dict(size=14),
        hovermode="x unified"
    )

    return fig

def multi_plot(ticker_list, start, end):
    fig = go.Figure()
    for tick in ticker_list:
        data = yf.download(tick, start=start, end=end)
        if not data.empty:
            fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name=tick))
    fig.update_layout(title="Multiple Stock Close Prices", xaxis_title="Date", yaxis_title="Price")
    return fig

# Load and process data
df = get_data(ticker, start_date, end_date)

if df.empty:
    st.warning("No data found for this ticker and date range.")
else:
    df = calculate_moving_average(df, ma_window)
    df = calculate_rsi(df, rsi_period)

    st.subheader(":scroll: Raw Data (Last 5 rows)")
    st.dataframe(df.tail())

    st.subheader(":chart_with_upwards_trend: Price Chart with Moving Average")
    st.plotly_chart(plot_price(df, ticker), use_container_width=True)

    st.subheader(":bar_chart: Daily Trading Volume")
    st.plotly_chart(plot_volume(df, ticker), use_container_width=True)

    st.subheader(":thermometer: RSI Indicator")
    st.plotly_chart(plot_rsi(df, ticker), use_container_width=True)

    # CSV download
    csv = df.to_csv().encode("utf-8")
    st.download_button(
        label="📅 Download Data as CSV",
        data=csv,
        file_name=f"{ticker}_data.csv",
        mime="text/csv"
    )

# Optional: Compare multiple stocks
tickers_input = st.sidebar.text_input("Compare Tickers (comma-separated)", value="AAPL,TSLA")
compare = st.sidebar.checkbox("Show Comparison Chart")

if compare:
    ticker_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    st.subheader(":bar_chart: Compare Multiple Stocks")
    st.plotly_chart(multi_plot(ticker_list, start_date, end_date), use_container_width=True)
