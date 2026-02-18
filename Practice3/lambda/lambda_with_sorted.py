#1
numbers=[8,6,9,4,5]
sorted_numbers=sorted(numbers,key=lambda x:-x)
print(sorted_numbers)

#2
numbers=[2,-2,3,-8,4,5]
sorted_numbers=sorted(numbers,key=lambda x:abs(x))
print(sorted_numbers)

#3
students=[("zhanyia",18),("samal",19),("aru",18)]
sorted_students=sorted(students,key=lambda x:x[1])
print(sorted_students)

#4
cities=["paris","spain","stambul"]
sorted_cities=sorted(cities,key=lambda word:len(word))
print(sorted_cities)