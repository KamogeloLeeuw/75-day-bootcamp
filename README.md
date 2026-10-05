## Week 1 -  Python foundations

### What I built this week
- day2_python_basics.py: fundamentals practice: data types, lists, dicts, oops, functions
- day3_file_io.py: CSV reading and writing with error handling
- day4_oop.py: is an employee class with salary calculations and CSV export
- employee_report.py: reads a CSV of employee data, cleans it, runs summary calculations, and prints a formatted report to the terminal and saves it to a file

### What I learned
- Python data types, string methods, file I/O, error handling, OOP basics, and Git branching with conventional commits
- The biggest thing that clicked was understanding how classes connect to real data structures, the Employee class maps directly to the employees table I built in PostgreSQL last month

### Reflection
Folder naming caused a git headache early on, `week1 python-foundations` with a space broke every `git add` command. Fixed by renaming the folder 
Lesson: no spaces in folder names ever

OOP took a while to click. The syntax wasn't the hard part, understanding why you'd use a class instead of just a function was. It started making sense when I connected it to the Employee table in my PostgreSQL database. A class is just a blueprint for a row, and the methods are the things you'd do with that data.