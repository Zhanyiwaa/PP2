#1
class Animal:
    def sound(self):
        print("Animal sound")

class Cat(Animal):
    def sound(self):
        print("Meow")

Cat().sound()


#2
class Vehicle:
    def move(self):
        print("Vehicle moving")

class Bike(Vehicle):
    def move(self):
        print("Bike riding")

Bike().move()


#3
class Shape:
    def area(self):
        print("Unknown area")

class Square(Shape):
    def area(self):
        print("Area = side * side")

Square().area()


#4
class Person:
    def role(self):
        print("Person")

class Student(Person):
    def role(self):
        print("Student")

Student().role()
