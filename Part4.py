# Part 4:
score = int(input("Enter score: ")) # int() is used to ensure the input is treated as a number (integer) for comparison
if score >= 90: # always put colon at the end of an if/elif/else statement
    print("Grade A")
elif score >= 80: # Use "elif" not "else if" when checking multiple conditions in a chain
    print("Grade B")
elif score >= 70: # Use "elif" not "else if" when checking multiple conditions in a chain
    print("Grade C")
else: # always put colon at the end of an if/elif/else statement
    print("Grade F")