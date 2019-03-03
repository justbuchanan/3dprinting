#!/usr/bin/env python3

w = 34.0  # total width of tube
n = 7  # number of holes in two outer tubest. Inner tube has one less

c2c = w / n  # center-to-center spacing between cups


# We're dealing with inches, so we want to print sixteenths for the remainder instead of a decimal.
def format_num(x):
    return "{} + {}/16".format(int(x), int((x - int(x)) * 16))


print("Outer (with %d cups):" % n)
print("\n".join([format_num(2.5 + c2c * i) for i in range(n)]))

print()

print("Inner (with %d cups):" % (n - 1))
x0 = 2.5 + c2c / 2
print("\n".join([format_num(x0 + c2c * i) for i in range(n - 1)]))
