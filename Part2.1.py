# Part 2.1
score = float(input("Enter your score (0-100): "))
if 90 <= score <= 100:
    print("Your grade is: A")
elif 80 <= score < 90:
    print("Your grade is: B")
elif 70 <= score < 80:
    print("Your grade is: C")
elif 60 <= score < 70:
    print("Your grade is: D")
else:
    print("Below 60: F")