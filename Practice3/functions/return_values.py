#1
def square(x):
    return x**2
print(square(2))

#2
def full_name(first,last):
    return f"{first} {last}"
print(full_name("viki","woker"))

#3
def even_numbers(numbers):
    return [n for n in numbers if n%2==0]
print(even_numbers([1,2,3,4,5,6,7,8,9]))

#4
def create_user(name,age):
    return {"name":name,"age":age}
print(create_user("murka",3))