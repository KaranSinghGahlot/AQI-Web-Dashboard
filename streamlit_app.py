import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit Page Config
st.set_page_config(page_title="Air Quality Monitoring", layout="wide")

# Title
st.title("🌍 Air Quality Monitoring")

# Sidebar for Date Selection
col1, col2, col3 = st.columns([3, 3, 2])
start_date = col1.date_input("Start Date", pd.to_datetime("2025-01-01"))
end_date = col2.date_input("End Date", pd.to_datetime("2025-01-31"))
aggregation = col3.selectbox("Aggregation", ["Daily", "Hourly"])

# Dummy Data (Replace this with real-time or database data)
dates = pd.date_range(start=start_date, end=end_date, freq='D')
df = pd.DataFrame({
    "Date": dates,
    "NOX": [20 + i % 10 * 5 for i in range(len(dates))],
    "NO": [10 + i % 5 * 3 for i in range(len(dates))],
    "NO2": [15 + i % 7 * 2 for i in range(len(dates))]
})

# Plot Data
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Date"], df["NOX"], label="NOX", color='red', marker='o')
ax.plot(df["Date"], df["NO"], label="NO", color='blue', marker='o')
ax.plot(df["Date"], df["NO2"], label="NO2", color='green', marker='o')

ax.set_xlabel("Date")
ax.set_ylabel("Concentration")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Statistics Section
st.subheader("📊 Statistics")
col1, col2, col3 = st.columns(3)

col1.metric("NOX Concentration", f"Min: {df['NOX'].min()} | Max: {df['NOX'].max()} | Mean: {df['NOX'].mean():.2f}")
col2.metric("NO Concentration", f"Min: {df['NO'].min()} | Max: {df['NO'].max()} | Mean: {df['NO'].mean():.2f}")
col3.metric("NO2 Concentration", f"Min: {df['NO2'].min()} | Max: {df['NO2'].max()} | Mean: {df['NO2'].mean():.2f}")

# Run Streamlit
# In terminal, execute:
# streamlit run streamlit_app.py
