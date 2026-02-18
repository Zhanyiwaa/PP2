#1
def say_hello():
    print("hello")

say_hello()

#2
def greet(name):
    print(f"hello,{name}")

greet("anna")

#3
def add(a,b):
    return a+b

print(add(2,3))

#4
def prints_list(items):
    for item in items:
        print(item)

prints_list(["apple","banana","cherry"])