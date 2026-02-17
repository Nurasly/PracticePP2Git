import math

# Method 1: Simple formula
degree = float(input("Input degree: "))
radian = degree * math.pi / 180

print(f"Output radian: {radian:.6f}")


# Alternative one-liner style (also fine):
# print(f"Output radian: {float(input('Input degree: ')) * math.pi / 180:.6f}")


print("Area of a trapezoid calculator")
h = float(input("Height: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))

area = (b1 + b2) * h / 2

print(f"Expected Output: {area}")


import math

print("Regular polygon area calculator")
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

# Formula: Area = (n × s²) / (4 × tan(π/n))
area = (n * s ** 2) / (4 * math.tan(math.pi / n))

print(f"The area of the polygon is: {area:.0f}")
# or print(f"The area of the polygon is: {round(area)}")  # also common


print("Parallelogram area calculator")
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height

print(f"Expected Output: {area}")
# or print(f"Expected Output: {area:.1f}") if you always want one decimal


