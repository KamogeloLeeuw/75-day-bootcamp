# Debugging note: the original SAPS .xlsm file had merged cells 
# Switch to Titanic dataset for a better example pandas learning

import pandas as pd

df = pd.read_csv("week2/raw_data.csv")

# shape
print("=== SHAPE ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# column names
print("=== COLUMN NAMES ===")
print(df.columns.tolist())

# data types
print("\n=== DATA TYPES ===")
print(df.dtypes)

# missing values
print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

# basic statistics  
print("\n=== BASIC STATISTICS ===")
print(df.describe())

# rows
print("\n=== ROWS ===")
print(df.head())