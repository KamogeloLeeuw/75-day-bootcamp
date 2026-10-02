import csv
class Employee:
    def __init__(self, name, department, salary):
        self.name = name
        self.department = department
        self.salary = salary

    def __str__(self):
        return f"{self.name} | {self.department} | R{self.salary:,.2f}"

    # annual salary
    def annual_salary(self):
        return self.salary * 12
    
    # salary increase
    def apply_raise(self, percent):
        self.salary = self.salary * (1 + percent / 100)
        return self.salary

    def to_dict(self):
        return {
            "name": self.name,
            "department": self.department,
            "salary": self.salary,
            "annual_salary": self.annual_salary()
        }

# Testing it
employees = [
    Employee("Tshiamo Mamabolo", "HR", 15000),
    Employee("Linda Leso", "IT", 25000),
    Employee("Luke Smith", "Finance", 36000),
    Employee("James van Wyk", "IT", 22000)
]

for ep in employees:
    print(ep)

# increase in salary (a raise)
employees[2].apply_raise(10)
print(f"\nAfter raise: {employees[2]}")

# export to csv
with open("employees_oop.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "department", "salary", "annual_salary"])
    writer.writeheader()
    for ep in employees:
        writer.writerow(ep.to_dict())