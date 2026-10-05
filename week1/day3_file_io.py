# file I/O, csv, error handling

import csv

# 1. Creating a list of employees; each has a name, department and salary
data = [
    ["name", "department", "salary"],
    ["James van Wyk", "IT", 10000],
    ["Lebogang Mahapu", "Finance", 12500],
    ["Linda Leso", "Finance", 8500],
    ["Tshiamo Mamabolo", "Sales", 15000],
    ["Luke Smith", "HR", 25000],
    ["Karabo Khumalo", "Marketing", 9000],
]

# 2. Writing them to a CSV file
with open("employees.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("File written successfully")

# 3. Read the file back using csv.DictReader and print each row
print("\n--- Reading Employees CSV ---")
with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(dict(row))  # converted to a regular dict for reading

# Error handling 
print("\n--- Error Handling Test ---")
try:
    with open("nonexistent.csv", "r") as f:
        content = f.read()

except FileNotFoundError:
    print("Error: the requested file could not be found")

finally:
    print("Done")