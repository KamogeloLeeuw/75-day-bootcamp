import os
import pandas as pd
import numpy as np

def clean_data(input_path='week2/raw_data.csv', output_path='week2/clean_data.csv'):

    # read raw data
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Missing file: {input_path}")

    df = pd.read_csv(input_path)

    # Print shape and missing values
    print("=== Before Cleaning ===")
    print(f"Dataset Shape: {df.shape}")
    print("\nMinnsinf Value Counts: ")
    print(df.isnull().sum())
    print("-" * 30)

    # drop cabin and passengerid
    df = df.drop(columns=['Cabin', 'PassengerId'], errors='ignore')

    # fill missing age values with the median age
    median_age = df['Age'].median()
    df['Age'] = df['Age'].fillna(median_age)

    # fill missing embarked values with the mode
    if not df['Embarked'].mode().empty:
        mode_embarked = df['Embarked'].mode()[0]
        df['Embarked'] = df['Embarked'].fillna(mode_embarked)

    # strip whitespace from string columns
    string_columns = df.select_dtypes(include=['str']).columns
    for col in string_columns:
        df[col] = df[col].astype(str).str.strip()

    # print shape and missing values after cleaning
    print("=== AFTER CLEANING ===")
    print(f"Dataset Shape: {df.shape}")
    print("\nMissing Value Counts:")
    print(df.isnull().sum())
    print("-" * 30)

    # save the cleaned data to a new CSV file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Process completed. File saved to {output_path}")

if __name__ == "__main__":
    clean_data()