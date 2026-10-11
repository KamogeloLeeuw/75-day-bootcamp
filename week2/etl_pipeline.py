from pathlib import Path

import pandas as pd

# Required columns for the ETL process
REQUIRED_COLUMNS = ["Survived", "Pclass", "Sex", "Age", "Fare"]


def ingest(filepath):
    # Read the raw CSV file
    return pd.read_csv(filepath)


def validate(df):
    # Checking if all required columns are present in the dataframe
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required column(s): {', '.join(missing_columns)}"
        )

    if df.empty:
        raise ValueError("The input dataset contains no rows")


def clean(df):
    """Drop unnecessary columns, strip whitespace, and fill missing values."""

    # use a copy of the dataframe so that the original is not changed
    cleaned_df = df.copy()

    # unnecessary columns are dropped
    cleaned_df = cleaned_df.drop(
        columns=["Cabin", "PassengerId"],
        errors="ignore",
    )

    # removing whitespace from text and filling missing values
    text_columns = cleaned_df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned_df[column] = cleaned_df[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
        cleaned_df[column] = cleaned_df[column].replace("", pd.NA)

    # fill missing values for numeric and categorical columns
    for column in cleaned_df.columns:
        if cleaned_df[column].isna().any():
            if pd.api.types.is_numeric_dtype(cleaned_df[column]):
                fill_value = cleaned_df[column].median()
                if pd.isna(fill_value):
                    fill_value = 0
            else:
                most_common = cleaned_df[column].mode(dropna=True)
                if not most_common.empty:
                    fill_value = most_common.iloc[0]
                else:
                    fill_value = "Unknown"

            cleaned_df[column] = cleaned_df[column].fillna(fill_value)

    return cleaned_df


def transform(df):
    """Add AgeGroup and FareCategory columns to the DataFrame."""
    transformed_df = df.copy()

    # grouping passengers by age
    age_bins = [0, 12, 18, 35, 60, float("inf")]
    age_labels = [
        "Child (12 & under)",
        "Teen (13-18)",
        "Young adult (19-35)",
        "Adult (36-60)",
        "Senior (over 60)",
    ]

    transformed_df["AgeGroup"] = pd.cut(
        transformed_df["Age"],
        bins=age_bins,
        labels=age_labels,
        right=True,
        ordered=True,
    )

    # grouping passengers by ticket fare
    fare_bins = [0, 10, 30, 100, float("inf")]
    fare_labels = [
        "Budget (<10)",
        "Standard (10-29.99)",
        "Premium (30-99.99)",
        "Luxury (100+)",
    ]

    transformed_df["FareCategory"] = pd.cut(
        transformed_df["Fare"],
        bins=fare_bins,
        labels=fare_labels,
        right=False,
        ordered=True,
    )

    return transformed_df


def aggregate(df):
    """Return summary DataFrames for overall results and passenger groups"""
    passenger_count = len(df)
    survivor_count = int((df["Survived"] == 1).sum())
    death_count = int((df["Survived"] == 0).sum())

    survival_rate = (
        survivor_count / passenger_count * 100
        if passenger_count
        else 0
    )

    # overall stats
    overall_summary = pd.DataFrame(
        {
            "Metric": [
                "Total passengers",
                "Survivors",
                "Deaths",
                "Survival rate (%)",
                "Average age",
                "Average fare",
            ],
            "Value": [
                str(passenger_count),
                str(survivor_count),
                str(death_count),
                f"{survival_rate:.2f}%",
                f"{df['Age'].mean():.2f} years",
                f"{df['Fare'].mean():.2f}",
            ],
        }
    )

    # survival stats by sex
    survival_by_sex = (
        df.groupby("Sex", dropna=False, observed=False)
        .agg(
            Passengers=("Survived", "size"),
            Survivors=("Survived", "sum"),
            SurvivalRate=("Survived", "mean"),
        )
        .reset_index()
    )

    survival_by_sex["Survival rate (%)"] = (
        survival_by_sex.pop("SurvivalRate") * 100
    ).round(2)

    # survival stats by passenger class
    survival_by_class = (
        df.groupby("Pclass", dropna=False, observed=False)
        .agg(
            Passengers=("Survived", "size"),
            Survivors=("Survived", "sum"),
            SurvivalRate=("Survived", "mean"),
        )
        .reset_index()
    )

    survival_by_class["Survival rate (%)"] = (
        survival_by_class.pop("SurvivalRate") * 100
    ).round(2)

    # number of passengers per age group
    passengers_by_age_group = (
        df.groupby("AgeGroup", observed=False)
        .size()
        .rename("Passengers")
        .reset_index()
    )

    # fare stats and survival rates by fare category
    fare_category_summary = (
        df.groupby("FareCategory", observed=False)
        .agg(
            Passengers=("Survived", "size"),
            AverageFare=("Fare", "mean"),
            SurvivalRate=("Survived", "mean"),
        )
        .reset_index()
    )

    fare_category_summary["Average fare"] = (
        fare_category_summary.pop("AverageFare")
    ).round(2)

    fare_category_summary["Survival rate (%)"] = (
        fare_category_summary.pop("SurvivalRate") * 100
    ).round(2)

    # store the summaries in a dictionary for the report
    return {
        "Overall summary": overall_summary,
        "Survival by sex": survival_by_sex,
        "Survival by passenger class": survival_by_class,
        "Passengers by age group": passengers_by_age_group,
        "Fare category summary": fare_category_summary,
    }


def generate_report(stats):
    """Format the summary DataFrames as a business-style text report"""
    sections = [
        "TITANIC PASSENGER ANALYTICS REPORT",
        "=" * 36,
        "Summary of passenger numbers, survival patterns, age groups, and fares",
    ]

    # converting each summary table into readable text
    for section_name, summary_df in stats.items():
        sections.extend(
            [
                "",
                section_name.upper(),
                "-" * len(section_name),
                summary_df.to_string(index=False),
            ]
        )

    sections.extend(
        [
            "",
            "Notes:",
            "- Survival rates are shown as percentages",
            "- Age and fare categories are grouped into ranges for easier comparison",
        ]
    )

    return "\n".join(sections) + "\n"


def run_pipeline(filepath):
    """Run each ETL step, export the files, and handle common errors"""
    output_dir = Path(__file__).resolve().parent
    input_path = Path(filepath)

    # support running the script from the project root or elsewhere
    if not input_path.is_absolute() and not input_path.exists():
        project_root_candidate = output_dir.parent / input_path
        script_dir_candidate = output_dir / input_path.name

        if project_root_candidate.exists():
            input_path = project_root_candidate
        elif script_dir_candidate.exists():
            input_path = script_dir_candidate

    try:
        print("Step 1/6: Ingesting raw data...")
        df = ingest(input_path)

        print("Step 2/6: Validating required columns...")
        validate(df)

        print("Step 3/6: Cleaning data...")
        cleaned_df = clean(df)

        print("Step 4/6: Transforming data...")
        transformed_df = transform(cleaned_df)

        print("Step 5/6: Aggregating summary statistics...")
        stats = aggregate(transformed_df)

        print("Step 6/6: Exporting data and report...")

        # save the cleaned and transformed dataset
        output_csv = output_dir / "pipeline_output.csv"
        transformed_df.to_csv(output_csv, index=False)

        # generate and save the text report
        output_report = output_dir / "pipeline_report.txt"
        report_text = generate_report(stats)

        output_report.write_text(
            report_text,
            encoding="utf-8",
        )

        print(f"Saved transformed data: {output_csv}")
        print(f"Saved summary report: {output_report}")
        print("Pipeline completed successfully")

        return stats

    except FileNotFoundError:
        print(f"Error: input file not found: {input_path}")

    except ValueError as error:
        print(f"Pipeline error: {error}")

    return None


if __name__ == "__main__":
    run_pipeline("week2/raw_data.csv")