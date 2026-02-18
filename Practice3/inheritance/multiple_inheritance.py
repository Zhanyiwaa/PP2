#1
class A:
    def method1(self):
        print("A")

class B:
    def method2(self):
        print("B")

class C(A, B):
    pass

obj = C()
obj.method1()
obj.method2()


#2
class Father:
    def skill1(self):
        print("Driving")

class Mother:
    def skill2(self):
        print("Cooking")

class Child(Father, Mother):
    pass

Child().skill1()
Child().skill2()


#3
class X:
    def hello(self):
        print("Hello from X")

class Y:
    def hello(self):
        print("Hello from Y")

class Z(X, Y):
    pass

Z().hello()  # MRO


#4
class Writer:
    def write(self):
        print("Writing")

class Speaker:
    def speak(self):
        print("Speaking")

class Person(Writer, Speaker):
    pass

p = Person()
p.write()
p.speak()
