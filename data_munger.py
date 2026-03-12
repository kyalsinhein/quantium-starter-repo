import pandas as pd
import glob
import os

# Path to your data folder
data_folder = "data"

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(data_folder, "*.csv"))

# List to hold processed DataFrames
processed_dfs = []

# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)

    # Normalise column names
    df.columns = df.columns.str.strip().str.lower()

    # Filter only Pink Morsels (case-insensitive)
    df = df[df['product'].str.lower() == 'pink morsel']

    # Strip '$' from price and convert to float
    df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)

    # Calculate Sales
    df['sales'] = df['quantity'] * df['price']

    # Keep only required columns
    df = df[['sales', 'date', 'region']]

    processed_dfs.append(df)

# Combine all processed data
combined_df = pd.concat(processed_dfs, ignore_index=True)

# Sort by date
combined_df = combined_df.sort_values('date').reset_index(drop=True)

# Save to a new CSV
combined_df.to_csv("pink_morsel_sales.csv", index=False)

print(f"Processed CSV saved as pink_morsel_sales.csv ({len(combined_df)} rows)")