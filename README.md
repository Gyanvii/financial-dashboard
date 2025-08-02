# Financial Dashboard
This project is a fully interactive financial dashboard built using Streamlit. It allows users to explore historical stock performance, visualize key technical indicators like RSI and Moving Averages, and gain better insights into market trends through dynamic and user-friendly visualizations.

## Overview
The financial dashboard was designed to help investors, students, and finance enthusiasts analyze stock data in a meaningful way. It fetches live financial data using the `yfinance` library and provides visual representations using Plotly, making technical analysis accessible even to beginners.

## Features
- Input any stock symbol and view live financial data
- Visualize technical indicators like:
  - Relative Strength Index (RSI)
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
- View interactive candlestick charts to analyze market trends
- Explore daily open, close, high, low, and volume data
- Option to switch between different time ranges (e.g., 1 month, 3 months, 6 months, 1 year)

## **Technologies Used**
- Python
- Streamlit
- yfinance
- Pandas
- NumPy
- Plotly

## **Project Structure**
financial-dashboard/
├── financial_dashboard.py     # Main Streamlit application file
├── requirements.txt           # List of Python packages required
├── .streamlit/
│   └── config.toml            # Streamlit configuration settings
└── README.md                  # Project documentation

## **Future Improvements**
Add more technical indicators (MACD, Bollinger Bands)
Compare multiple stocks on the same graph
Allow users to download reports or charts
Enhance responsiveness for mobile devices

## **About the Creator**
Built by Gyanvi Agarwal – a final-year Computer Science and Engineering student at VIT, passionate about data science, finance, and building impactful tech projects.

## **License**
This project is open source and available under the MIT License. You are free to use, modify, and distribute it with proper attribution.
