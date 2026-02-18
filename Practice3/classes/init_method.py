#1
class Student:
    def __init__(self,name):
        self.name=name

s=Student("arya")
print(s.name)

#2
class Car:
    def __init__(self,brand,year):
        self.brand=brand
        self.year=year

c=Car("Toyota",2022)
print(c.brand,c.year)

#3
class Dog:
    def __init__(self,name,age):
        self.name=name
        self.age=age

d=Dog("barsik",3)
print(d.name,d.age)

#4
class Account:
    def __init__(self,balance):
        self.balance=balance

acc=Account(1000)
print(acc.balance)
