import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go

# --- Load and Prepare Data ---
BASE_DIR = r"C:\Users\ajmer\OneDrive\Desktop\NPL Project\AQI Web Dashboard\data"
DATA_FILE = os.path.join(BASE_DIR, "2025 Merged Data.xlsx")

df = pd.read_excel(DATA_FILE, engine="openpyxl")
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df.set_index('time', inplace=True)
df.sort_index(inplace=True)

pollutant_cols = ["NOX Conc", "NO Conc", "NO2 Conc"]

def compute_statistics(data):
    stats = {}
    for col in pollutant_cols:
        stats[col] = {
            "min": round(data[col].min(), 2),
            "max": round(data[col].max(), 2),
            "mean": round(data[col].mean(), 2)
        }
    return stats

# --- Streamlit UI ---
st.set_page_config(page_title="Air Quality Monitoring Dashboard", layout="wide")
st.title("Air Quality Monitoring Dashboard")

# Use separate date and time inputs for precise selection
st.subheader("Select Date & Time Range")
default_start_date = df.index.min().date()
default_start_time = df.index.min().time()
default_end_date = df.index.max().date()
default_end_time = df.index.max().time()

start_date = st.date_input("Start Date", value=default_start_date)
# Set step to 60 seconds (1 minute) as it's the minimum allowed.
start_time = st.time_input("Start Time", value=default_start_time, step=timedelta(minutes=1))
end_date = st.date_input("End Date", value=default_end_date, min_value=start_date)
end_time = st.time_input("End Time", value=default_end_time, step=timedelta(minutes=1))

# Combine date and time into datetime objects
start_datetime = datetime.combine(start_date, start_time)
end_datetime = datetime.combine(end_date, end_time)

aggregation = st.selectbox("Aggregation", 
                           options=["raw", "minutely", "hourly", "daily", "weekly", "monthly"],
                           index=3)

# Initialize data_filtered to None
data_filtered = None

if st.button("Fetch Data"):
    try:
        data_filtered = df.loc[start_datetime:end_datetime]
        if data_filtered.empty:
            st.error("No data available for the selected date range.")
        else:
            aggregation_map = {
                "raw": None,
                "minutely": "T",
                "hourly": "H",
                "daily": "D",
                "weekly": "W",
                "monthly": "M"
            }
            if aggregation != "raw":
                data_filtered = data_filtered.resample(aggregation_map[aggregation]).mean().dropna().interpolate()
            
            stats = compute_statistics(data_filtered)
            
            st.subheader("Statistics")
            col1, col2, col3 = st.columns(3)
            col1.metric("NOX Concentration", f"{stats['NOX Conc']['mean']}", 
                        f"Min: {stats['NOX Conc']['min']} / Max: {stats['NOX Conc']['max']}")
            col2.metric("NO Concentration", f"{stats['NO Conc']['mean']}", 
                        f"Min: {stats['NO Conc']['min']} / Max: {stats['NO Conc']['max']}")
            col3.metric("NO2 Concentration", f"{stats['NO2 Conc']['mean']}", 
                        f"Min: {stats['NO2 Conc']['min']} / Max: {stats['NO2 Conc']['max']}")
            
            st.subheader("Air Quality Trends")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data_filtered.index, y=data_filtered["NOX Conc"],
                                     mode='lines+markers', name="NOX", line=dict(color='red')))
            fig.add_trace(go.Scatter(x=data_filtered.index, y=data_filtered["NO Conc"],
                                     mode='lines+markers', name="NO", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=data_filtered.index, y=data_filtered["NO2 Conc"],
                                     mode='lines+markers', name="NO2", line=dict(color='green')))
            fig.update_layout(title="Air Quality Trends", xaxis_title="Time", 
                              yaxis_title="Concentration", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

if data_filtered is not None:
    with st.expander("Show Raw Data"):
        st.write(data_filtered.reset_index())
