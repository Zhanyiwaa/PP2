#1
class Dog:
    species="Canine"

d1=Dog()
print(Dog.species)

#2
class Cars:
    wheels=4

c1=Cars()
c2=Cars()
print(c1.wheels,c2.wheels)

#3
class School:
    country="Kazakhstan"

s=School()
print(s.country)

#4
class Student:
    school_name = "High School"

    def __init__(self, name):
        self.name = name

st = Student("Anna")
print(st.name)
print(Student.school_name)