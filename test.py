#import os

#DATA_FILE = r"C:\Users\ajmer\OneDrive\Desktop\NPL Project\AQI Web Dashboard\data\January 2025 data.xlsx"

#if os.path.exists(DATA_FILE):
#    print("✅ File found! Proceeding with reading...")
#else:
#    print("❌ File not found! Check the file path.")

from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Define the path to your Excel file
BASE_DIR = r"C:\Users\ajmer\OneDrive\Desktop\NPL Project\AQI Web Dashboard\data"
DATA_FILE = os.path.join(BASE_DIR, "2025 Merged Data.xlsx")

# Load the Excel file using pandas
try:
    df = pd.read_excel(DATA_FILE, engine="openpyxl")
except Exception as e:
    df = None
    print(f"Error loading Excel file: {e}")

df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
df.set_index('Time', inplace=True)

df.columns = df.columns.str.lower()
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df.set_index('time', inplace=True)
