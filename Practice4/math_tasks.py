import math
import random

#1.degree to radian 
d=float(input("Input degree: "))
r=math.radians(d)
print("Output radian: ",round(r,6))

#2.area of trapezoid
h=float(input("Height:"))
a=float(input("Base, first value:"))
b=float(input("Base, second value:"))
area=(a+b)*h/2
print("Expected Output: ",area )

#3.area of regular polygon 
n=int(input("Input number of side: "))
s=int(input("Input the length of a side: "))
area_polygon=(n * s**2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", int(area_polygon))

#4.area of parallelogram
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area_parallelogram = base * height
print("Expected Output:", float(area_parallelogram))

