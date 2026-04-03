# Part 2.1
score = float(input("Enter your score (0-100): "))
if score >= 90 and score <= 100:
    print("You grade is: A")
elif score >= 80 and score < 90:
    print("You grade is: B")
elif score >= 70 and score < 80:
    print("You grade is: C")
elif score >= 60 and score < 70:
    print("You grade is: D")
else:
    print("Below 60: F")