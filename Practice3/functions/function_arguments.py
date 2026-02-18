#1
def subtract(a,b):
    return a-b
print(subtract(10,6))

#2
def power(base,exp=2):
    return base**exp
print(power(3))
print(power(3,3))

#3
def introduce(name,age):
    print(f"my name is {name} and i am {age} years old")
introduce(age=19,name="lein")

#4
def describe_pet(name,animal="dog"):
    print(f"i have a {animal} named {name}")
describe_pet("luci")
describe_pet("muiza",animal="cat")