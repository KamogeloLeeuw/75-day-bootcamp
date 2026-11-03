import pandas as pd
import os

def ingest():
    """Create a sample dataset in memory."""
    data = {
        "name": ["Thabo Nkosi", "Naledi Mokoena", "Sipho Mahlangu",
                 "Zanele Dlamini", "Karabo Sithole"],
        "department": ["IT", "Finance", "HR", "IT", "Marketing"],
        "salary": [25000, 35000, 28000, 42000, 22000],
        "city": ["Johannesburg", "Pretoria", "Durban",
                 "Johannesburg", "Cape Town"]
    }
    return pd.DataFrame(data)

def transform(df):
    """Add annual salary and salary category columns."""
    df["annual_salary"] = df["salary"] * 12
    df["salary_category"] = df["salary"].apply(
        lambda x: "High" if x >= 35000 else "Medium" if x >= 25000 else "Low"
    )
    return df

def aggregate(df):
    """Return department summary statistics."""
    return df.groupby("department").agg(
        headcount=("name", "count"),
        avg_salary=("salary", "mean"),
        total_payroll=("salary", "sum")
    ).reset_index()

def write_to_postgres(df, summary):
    """Write results to PostgreSQL if connection details are available."""
    db_host = os.getenv("DB_HOST")
    if not db_host:
        print("No DB_HOST set — skipping database write.")
        return

    from sqlalchemy import create_engine

    db_url = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    engine = create_engine(db_url)
    df.to_sql("employees", engine, if_exists="replace", index=False)
    summary.to_sql("department_summary", engine, if_exists="replace", index=False)
    print("Data written to PostgreSQL successfully.")

def run_pipeline():
    """Run the full ETL pipeline."""
    print("Step 1/5: Ingesting data...")
    df = ingest()

    print("Step 2/5: Transforming data...")
    df = transform(df)

    print("Step 3/5: Aggregating...")
    summary = aggregate(df)

    print("Step 4/5: Writing to database...")
    write_to_postgres(df, summary)

    print("Step 5/5: Results:")
    print("\n--- Employee Data ---")
    print(df.to_string(index=False))
    print("\n--- Department Summary ---")
    print(summary.to_string(index=False))
    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()