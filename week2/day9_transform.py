# Debugging postmortem
# Error: KeyError 'Survived' in transform script
# Cause: raw_data.csv downloaded with a BOM (Byte Order Mark) character
#        which corrupted the first column name to 'fSurvived'
# Fix: added encoding='utf-8-sig' to pd.read_csv() which strips BOM automatically
# Lesson: always check column names after reading external files.
#         BOM encoding is common in files exported from Excel or Windows tools.

import pandas as pd

def transform_and_analysis(input_path='week2/clean_data.csv'):

    # read cleaned data
    df = pd.read_csv(input_path, encoding='utf-8-sig')
    print("Columns in clean_data.csv: ", df.columns.tolist())

    df.columns = df.columns.str.strip()

    # create age group
    age_bins = [0, 17, 35, 60, float('inf')]
    age_labels = ['Child', 'Young Adult', 'Adult', 'Senior']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, include_lowest=True)

    # fare category
    fare_bins = [0, 10, 50, float('inf')]
    fare_labels = ['Low', 'Medium', 'High']
    df['FareCategory'] = pd.cut(df['Fare'], bins=fare_bins, labels=fare_labels, include_lowest=True)

    # group by pclass and calculating the mean age and fare
    class_analysis = df.groupby('Pclass')[['Fare', 'Age']].mean()

    # group by gender and calculate the survival rate
    gender_analysis = df.groupby('Sex')['Survived'].mean()

    # group by age group and calculate the survival rate
    age_group_analysis = df.groupby('AgeGroup', observed=False)['Survived'].mean()

    df.to_csv('week2/transformed_data.csv', index=False)

    # print results
    print("-" * 50)
    print("Analysis Results")
    print("-" * 50)

    print("\n[1] Mean Fare and Age by Passanger Class:")
    print(class_analysis)
    print("-" * 50)

    print("\n[2] Survival Rate by Age Group:")
    print(age_group_analysis)
    print("=" * 50)

    print("\n[3] Survival Rate by Gender:")
    print(gender_analysis)
    print("=" * 50)


if __name__ == "__main__":
    transform_and_analysis()