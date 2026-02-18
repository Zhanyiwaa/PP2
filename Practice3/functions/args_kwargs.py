#1
def sum_all(*numbers):
    return sum(numbers)
print(sum_all(1,2,3,4))

#2
def show_args(*args):
    for arg in args:
        print(arg)
print(show_args("a","b","c"))

#3
def show_profile(**kwargs):
    for key,value in kwargs.items():
        print(f"{key}: {value}")
show_profile(name="levi",age=35)

#4
def example_func(*args,**kwargs):
    print("args",args)
    print("kwargs",kwargs)
example_func(1,2,3,name="erwin",city="london")