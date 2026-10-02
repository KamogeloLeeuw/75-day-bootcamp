# write:

# 1. Variables and data types (4 variables: 1 string, 1 int, 1 float, 1 boolean)
name = "Kamogelo"
age = 23
salary = 15000.00
is_student = False

print("--- Variable types ---")
print(type(name))
print(type(age))
print(type(salary))
print(type(is_student))


# 2. string methods
print("\n--- String methods ---")
print(name.upper())  #print in CAPS
print(name.lower())  #print in lower case
print(name.replace("a", "o"))  #replace letters

# 3. list of 5 SA cites, print the list
cities = ["Pretoria", "Durban", "Gqeberha", "Bloemfontein", "Klerksdorp"]
cities.append("Cape Town")  #appended new city 

print("\n--- Cities list & length ---")
print(cities)
print(len(cities))

# 4. a dictionary representing: name, city age, is a student
myself = {
    "name": "Kamogelo",
    "city": "Klerksdrop",
    "age": 20,
    "is_student": False
}
myself["is_student"] = True 

print("\n--- Updated dictionary ---")
print(myself)

# 5.for loop over the city lists that prints each city in uppercase
for city in cities:
    print(city.upper())

# 6.a function called calculate_annual_salary
def calculate_annual_salary(monthly_salary):
    return monthly_salary * 12

annual_res = calculate_annual_salary(15000)

print("\n--- Annual Salary Calculation ---")
print(f"Annual salary: R{annual_res:,.2f}")