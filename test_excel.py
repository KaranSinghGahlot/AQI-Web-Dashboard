import pandas as pd

# Adjust the file path if your Excel file is in a subfolder
df = pd.read_excel("January 2025 data.xlsx", engine="openpyxl")
print(df.head())

print("Min date in dataset:", df.index.min())
print("Max date in dataset:", df.index.max())
