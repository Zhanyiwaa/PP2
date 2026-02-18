#1
class Animal:
    def speak(self):
        print("Sound")

class Dog(Animal):
    pass

Dog().speak()


#2
class Vehicle:
    def move(self):
        print("Moving")

class Car(Vehicle):
    pass

Car().move()


#3
class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    pass

Student().greet()


#4
class Shape:
    def info(self):
        print("Shape")

class Circle(Shape):
    pass

Circle().info()
