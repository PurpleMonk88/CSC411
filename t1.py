s = input("Enter an Integer: ")
try:
    i = int(s)
    print("Valid integer added:",i)
except ValueError as Err:
    print(Err)	