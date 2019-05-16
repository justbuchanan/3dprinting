#!/usr/bin/env python3

# A script to print out the locations for the cup holes in each tube. The holes
# will be 2" in diameter and evenly-spaced along the tube. The parameters below
# can be modified for other configurations.

w = 34.0  # total width of tube
n = 7  # number of holes in two outer tubes. Inner tube has one less

c2c = w / n  # horizontal center-to-center spacing between cups

# We're dealing with inches, so we want to print sixteenths for the remainder
# instead of a decimal.
def format_num(x):
    return "{} + {}/16".format(int(x), int((x - int(x)) * 16))


# x position of first cup (for the two outer tubes)
x0 = c2c / 2.0

print("Outer (with %d cups):" % n)
print("\n".join([format_num(x0 + c2c * i) for i in range(n)]))
print()
print("Inner (with %d cups):" % (n - 1))
print("\n".join([format_num(x0 + c2c * (i + 1 / 2)) for i in range(n - 1)]))
