# write:

# 1. Variables and data types (4 variables: 1 string, 1 int, 1 float, 1 boolean)
name = "Kamogelo"
age = 23
salary = 7500.00
is_employed = False

print(type(name), type(age), type(salary), type(is_employed))

# 2. string method
print(name.upper())
print(name.lower())
print(f"My name is {name} and I am {age} years old")

# 3. list of 5 SA cites, print the list
cities = ["Pretoria", "Durban", "Gqeberha", "Bloemfontein", "Klerksdorp"]
cities.append("Gqeberha")
print(cities)
print(cities[0])
print(len(cities))

# 4. a dictionary representing me: name, city age, is a student
employee = {
    "name": "Kamogelo",
    "city": "Klersdrop",
    "salary": 7500
}

print (employee["name"])
employee["salary"] = 12500
print(employee)

# for loop over the city lists that prints each city in uppercase
cities = ["Pretoria", "Durban", "Gqeberha", "Bloemfontein", "Klerksdorp"]

for city in cities:
    print(city.upper())

# a function called calculate_annual_salary
def calculate_annual_salary(monthly):
    return monthly * 12

print(f"Annual salary: R{calculate_annual_salary(12500):,.2f}")