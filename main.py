y = 3


def print_stuff():
    print("Calling print_stuff")
    print(y)
    z = 4
    print(z)
    print("exiting print_stuff")


print_stuff()  # we call print_stuff and the program execution goes to (***)
print(y)  # works fine
print(z)  # NameError!!!