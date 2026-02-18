#1
class Person:
    def __init__(self, name):
        self.name = name

class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

t = Teacher("Mr. Smith", "Math")
print(t.name, t.subject)


#2
class Animal:
    def __init__(self, species):
        self.species = species

class Dog(Animal):
    def __init__(self, species, name):
        super().__init__(species)
        self.name = name

d = Dog("Canine", "Buddy")
print(d.species, d.name)


#3
class A:
    def show(self):
        print("Class A")

class B(A):
    def show(self):
        super().show()
        print("Class B")

B().show()


#4
class Parent:
    def message(self):
        print("Parent")

class Child(Parent):
    def message(self):
        super().message()
        print("Child")

Child().message()
