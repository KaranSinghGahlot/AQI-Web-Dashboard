import pandas as pd
import glob
import os

# Define the directory where your monthly CSV files are stored
data_dir = r"C:\Users\ajmer\OneDrive\Desktop\NPL Project\data\2025"

# Pattern to match CSV files
csv_pattern = os.path.join(data_dir, '*.csv')

# Get a list of all CSV files in the directory
all_csv_files = glob.glob(csv_pattern)

# List to store individual DataFrames
df_list = []import pandas as pd
import glob
import os

# Define the directory where your monthly CSV files are stored.
data_dir = r'C:\Users\ajmer\OneDrive\Desktop\NPL Project\AQI Web Dashboard\data'

# Define the output directory and ensure it exists.
output_dir = r'C:\Users\ajmer\OneDrive\Desktop\NPL Project\AQI Web Dashboard\merged'
os.makedirs(output_dir, exist_ok=True)

# Pattern to match CSV files in the data directory.
csv_pattern = os.path.join(data_dir, '*.csv')

# Get a list of all CSV files in the directory.
all_csv_files = glob.glob(csv_pattern)

# List to store individual DataFrames.
df_list = []

# Read each CSV file into a DataFrame and add it to the list.
for file in all_csv_files:
    df = pd.read_csv(file)
    df_list.append(df)

# Concatenate all DataFrames into one DataFrame.
merged_df = pd.concat(df_list, ignore_index=True)

# Define the output file path.
output_file = os.path.join(output_dir, 'merged_data.csv')

# Save the merged DataFrame to a CSV file.
merged_df.to_csv(output_file, index=False)

print("All CSV files have been merged and saved at:", output_file)


# Read each CSV file into a DataFrame and add it to the list
for file in all_csv_files:
    df = pd.read_csv(file)
    df_list.append(df)

# Concatenate all DataFrames into one DataFrame
merged_df = pd.concat(df_list, ignore_index=True)

# Save the merged DataFrame to a single CSV file
merged_df.to_csv('/path/to/your/merged_data.csv', index=False)

print("All CSV files have been merged successfully!")
