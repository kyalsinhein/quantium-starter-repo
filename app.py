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
    
    # Filter only Pink Morsels
    df = df[df['product'] == 'Pink Morsel']
    
    # Calculate Sales
    df['Sales'] = df['quantity'] * df['price']
    
    # Keep only required columns
    df = df[['Sales', 'date', 'region']]
    
    # Append to list
    processed_dfs.append(df)

# Combine all processed data
combined_df = pd.concat(processed_dfs, ignore_index=True)

# Optional: sort by date for easier analysis
combined_df = combined_df.sort_values('date')

# Save to a new CSV
combined_df.to_csv("pink_morsel_sales.csv", index=False)

print("Processed CSV saved as pink_morsel_sales.csv")