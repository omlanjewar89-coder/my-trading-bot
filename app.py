import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import random
# Page Configuration
st.set_page_config(page_title="AI Trading Terminal", layout="wide",
page_icon="📈")
# Custom Styling
st.markdown("""
      <style>
      .main { background-color: #0e1117; color: white; }
      .stButton>button { width: 100%; border-radius: 10px; height: 3em;
  background-color: #2e7d32; color: white; }
      .report-box { background-color: #1e222d; padding: 20px; border-radius:
  15px; border: 1px solid #363a45; }
      </style>
      """, unsafe_allow_html=True)
  st.title("📈 AI Day-Trading Terminal")
  st.subheader("Free Research & Simulation Suite")
  # Sidebar Navigation
  menu = st.sidebar.selectbox("Choose a Tool", ["Chart Scanner", "Time
  Machine", "Risk Manager"])
  if menu == "Chart Scanner":
      st.header("🔍 Chart Scanner")
      ticker = st.text_input("Enter Ticker (e.g., TSLA, NVDA, AMD)",
  "TSLA").upper()
      if st.button("Scan for Setups"):
          with st.spinner(f"Analyzing {ticker}..."):
              # Fetch Data
              data = yf.download(ticker, period="1mo", interval="1d")

              if data.empty:
                  st.error("Could not find data for this ticker.")
              else:
                  # Basic Technical Analysis (Simulation of the 'Skills'
  logic)
                  close = data['Close']
                  ma20 = close.rolling(window=20).mean()
                  current_price = close.iloc[-1]
                  prev_price = close.iloc[-2]

                  # Setup Detection Logic
                  results = []
                  if current_price > ma20.iloc[-1]:
                      results.append("✅ Bullish Trend: Price is above
  20-day MA")

                  # Bull Flag approximation (Price consolidation after a
  run)
                  if (close.iloc[-5:].std() < close.iloc[-20:-5].std()):
                      results.append("🚩 Potential Bull Flag: Price is
  consolidating")

                  # Oversold Bounce (RSI approximation)
                  delta = close.diff()
                  gain = (delta.where(delta > 0,
  0)).rolling(window=14).mean()
                  loss = (-delta.where(delta < 0,
  0)).rolling(window=14).mean()
                  rs = gain / loss
                  rsi = 100 - (100 / (1 + rs))
                  if rsi.iloc[-1] < 35:
                      results.append("⚡ Oversold: Potential Bounce Setup")

                  st.markdown('<div class="report-box">',
  unsafe_allow_html=True)
                  st.write(f"**Analysis for {ticker}**")
                  if not results:
                      st.write("No clear high-probability setups found
  today.")
                  else:
                      for r in results:
                          st.write(r)
                  st.markdown('</div>', unsafe_allow_html=True)
                  st.line_chart(data['Close'])

  elif menu == "Time Machine":
      st.header("⏳ The Time Machine")
      st.write("Simulate 10,000 trading sessions based on historical
  volatility.")

      col1, col2 = st.columns(3)
      with col1:
          ticker = st.text_input("Ticker", "TSLA")
          entry = st.number_input("Entry Price", value=364.18)
      with col2:
          stop = st.number_input("Stop-Loss", value=358.32)
          target = st.number_input("Profit Target", value=370.04)

      if st.button("Run 10,000 Simulations"):
          with st.spinner("Simulating..."):
              # Fetch historical volatility
              data = yf.download(ticker, period="1y")
              daily_returns = data['Close'].pct_change().dropna()
              volatility = daily_returns.std()

              # Monte Carlo Simulation
              hits_target = 0
              hits_stop = 0
              neither = 0

              for _ in range(10000):
                  price = entry
                  hit = False
                  # Simulate 7 hours of trading (approx 60 mins intervals)
                  for _ in range(7):
                      change = np.random.normal(0, volatility)
                      price *= (1 + change)
                      if price >= target:
                          hits_target += 1
                          hit = True
                          break
                      if price <= stop:
                          hits_stop += 1
                          hit = True
                          break
                  if not hit:
                      neither += 1

              st.markdown('<div class="report-box">',
  unsafe_allow_html=True)
              st.write(f"### Simulation Results for {ticker}")
              st.write(f"🎯 **Target Reached First:**
  {(hits_target/10000)*100:.1f}%")
              st.write(f"🛑 **Stop-Loss Reached First:**
  {(hits_stop/10000)*100:.1f}%")
              st.write(f"⚪ **Neither Reached (Flat):**
  {(neither/10000)*100:.1f}%")
              st.markdown('</div>', unsafe_allow_html=True)

  elif menu == "Risk Manager":
      st.header("🛡️ Risk Manager")
      account = st.number_input("Account Balance ($)", value=1000)
      risk_pct = st.slider("Risk per Trade (%)", 0.1, 5.0, 1.0)
      stop_loss_dist = st.number_input("Distance to Stop Loss ($)",
  value=5.0)

      if st.button("Calculate Position Size"):
          amount_to_risk = account * (risk_pct / 100)
          shares = amount_to_risk / stop_loss_dist

          st.markdown('<div class="report-box">', unsafe_allow_html=True)
          st.write(f"**Risk Management Plan**")
          st.write(f"💰 Max Loss on this trade: ${amount_to_risk:.2f}")
          st.write(f"📦 Recommended Position Size: **{int(shares)}
  shares**")
          st.markdown('</div>', unsafe_allow_html=True)

  st.sidebar.markdown("---")
  st.sidebar.info("⚠️ **Trading is risky.** Use this for research and paper
  trading only.")
