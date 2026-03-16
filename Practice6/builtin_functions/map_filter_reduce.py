from functools import reduce
num=[1,2,3,4,5]

#1.map()-square numbers
s=list(map(lambda x:x*x,num))
print(s)

#2.map()-converts numbers to strings
str=list(map(str,num))
print(str)

#3.filter()-keep even numbers
e=list(filter(lambda x:x%2==0,num))
print(e)

#4.filter()-numbers greater than 3
g=list(filter(lambda x:x>3,num))
print(g)

#5.reduce()-sum of numbers
t=reduce(lambda a,b:a+b,num)
print(t)