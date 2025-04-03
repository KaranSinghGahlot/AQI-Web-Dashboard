from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

#Define the path to your Excel file
#BASE_DIR = r"C:\Users\ajmer\OneDrive\Desktop\NPL Project\AQI Web Dashboard\data"
#DATA_FILE = os.path.join(BASE_DIR, "January 2025 data.xlsx")

BASE_DIR = r"C:\Users\ajmer\OneDrive\Desktop\NPL Project\AQI Web Dashboard\data"
DATA_FILE = os.path.join(BASE_DIR, "2025 Merged Data.xlsx")
print("Updated file path:", DATA_FILE)

# Load the Excel file using pandas
df = pd.read_excel(DATA_FILE, engine="openpyxl")

# Convert the 'time' column to datetime and set it as the index
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df.set_index('time', inplace=True)
df.sort_index(inplace=True)

# Define the pollutant columns of interest
pollutant_cols = ["NOX Conc", "NO Conc", "NO2 Conc"]

def compute_statistics(data):
    """
    Compute min, max, and mean statistics for each pollutant column.
    """
    stats = {}
    for col in pollutant_cols:
        stats[col] = {
            "min": round(data[col].min(), 2),
            "max": round(data[col].max(), 2),
            "mean": round(data[col].mean(), 2)
        }
    return stats

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/data/aggregated")
def get_aggregated_data():
    agg = request.args.get("agg", "daily")  # Default to daily
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    
    # Copy the original DataFrame to apply filtering and resampling
    data_filtered = df.copy()

    if start_date and end_date:
        try:
            data_filtered = data_filtered.loc[start_date:end_date]
            if data_filtered.empty:
                return jsonify({"error": "No data available for the selected date range."}), 400
        except Exception as e:
            return jsonify({"error": f"Invalid date range: {str(e)}"}), 400

    # Resample (aggregate) based on the selected aggregation interval
    aggregation_map = {
        "raw": None,
        "minutely": "T",
        "hourly": "H",
        "daily": "D",
        "weekly": "W",
        "monthly": "M"
    }

    if agg in aggregation_map:
        if agg != "raw":
            data_filtered = data_filtered.resample(aggregation_map[agg]).mean().dropna().interpolate()
    else:
        return jsonify({"error": "Invalid aggregation type"}), 400

    # Keep only the pollutant columns of interest
    aggregated = data_filtered[pollutant_cols]

    # Compute statistics
    statistics = compute_statistics(aggregated)

    # Convert the aggregated DataFrame to JSON
    data_json = aggregated.reset_index()
    data_json['time'] = data_json['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    response = {
        "data": data_json.to_dict(orient="records"),
        "statistics": statistics
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
