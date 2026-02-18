#1
class Person:
    pass
p=Person()
print(type(p))

#2
class Car:
    def drive(self):
        print("driving")

c=Car()
c.drive()

#3
class Book:
    def info(self):
        return "book object"

b=Book()
print(b.info())

#4
class Animal:
    def sound(self):
        print("animal sound")

a=Animal()
a.sound()