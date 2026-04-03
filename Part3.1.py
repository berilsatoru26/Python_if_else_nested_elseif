# Part 3.1
username = input("Enter username: ")
password = input("Enter password: ")
if username == "admin":
    if password == "python123":
        print("Access granted! Welcome admin.")
    else:
        print("Incorrect password. Please try again.")
else:
    print("Invalid username or password. Please try again.")