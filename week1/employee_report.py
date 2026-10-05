"""
Employee Report CLI Tool
Description: Reads employee data from a CSV file, performs summary calculations, and outputs a report to the terminal and a file.

"""

import csv
import os

def read_and_clean(file_path):
    """
    Reads the CSV file using csv.DictReader and cleans whitespace
    Convert salary string to a float number
    """
    employees = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned_row = {
                "name": row["name"].strip(),
                "department": row["department"].strip(),
                "salary": float(row["salary"].strip()) 
            }

            employees.append(cleaned_row)

    return employees

def get_total_employees(employees):
    """Calculating the total number off employee in the dataset """
    return len(employees)

def get_total_payroll(employees):
    """ Calculating the sum of all the salaries"""
    return sum(ep["salary"] for ep in employees)

def get_average_salary(employees):
    """Calculates the average salary across all employees """
    if not employees:
        return 0.0
    return get_total_payroll(employees) / len(employees)

def get_highest_paid(employeess):
    """ Finding the highest paid employee and returns their name and salary """
    if not employeess:
        return None
    highest = max(employeess, key=lambda x: x["salary"])
    return highest["name"], highest["salary"]

def get_lowest_paid(employees):
    """Finding the lowest paid employee and returns their name and salary """
    if not employees:
        return None
    lowest = min(employees, key=lambda x: x["salary"])
    return lowest["name"], lowest["salary"]
    
def get_department_breakdown(employees):
    """
    Grouping employees by department
    Return number employees and total salaries per department
    """
    breakdown = {}
    for ep in employees:
        dept = ep["department"]
        salary = ep["salary"]
        if dept not in breakdown:
            breakdown[dept] = {"count": 0, "total_salary": 0.0}

        breakdown[dept]["count"] += 1
        breakdown[dept]["total_salary"] += salary

    return breakdown

def generate_report_text(stats):
    """
    Formatting the calculated statistics into a text report
    """
    report = []
    report.append("=" * 45)
    report.append("     EMPLOYEE SUMMARY REPORT     ")
    report.append("=" * 45)
    report.append(f"Total Employees:    {stats['total_count']}")
    report.append(f"Total Payroll:      R{stats['total_payroll']:,.2f}")
    report.append(f"Average Salary      R{stats['avg_salary']:,.2f}")
    report.append("=" * 45)
    report.append(f"Highest Paid Employee:      {stats['highest_name']} (R{stats['highest_salary']:,.2f})")
    report.append(f"Lowest Paid Employee:       {stats['lowest_name']} (R{stats['lowest_salary']:,.2f})")
    report.append("-" * 45)
    report.append("Department Breakdown: ")

    for dept, data in stats["breakdown"].items():
        report.append(f"    - {dept}: {data['count']} Employee(s) | Total Payroll: R{data['total_salary']:,.2f}")
    report.append("-" * 45)

    return "\n".join(report)

def main():
    csv_filename = "employees.csv"
    reprort_filename = "report.txt"

    try:
        # Reading and cleaning the data
        employees = read_and_clean(csv_filename)

        # Calculations
        stats = {
            "total_count": get_total_employees(employees),
            "total_payroll": get_total_payroll(employees),
            "avg_salary": get_average_salary(employees),
            "highest_name": get_highest_paid(employees)[0],
            "highest_salary": get_highest_paid(employees)[1],
            "lowest_name": get_lowest_paid(employees)[0],
            "lowest_salary": get_lowest_paid(employees)[1],
            "breakdown": get_department_breakdown(employees)
        }

        # Generate the text into the report
        report_text = generate_report_text(stats)

        # Print results
        print(report_text)

        # Write text into a file
        with open(reprort_filename, "w") as f:
            f.write(report_text)

    except FileNotFoundError:
        print(f"Error: Required source file '{csv_filename}' was not found")
        print("Run your previous setup script to generate the employee data first")

if __name__ == "__main__":
    main()