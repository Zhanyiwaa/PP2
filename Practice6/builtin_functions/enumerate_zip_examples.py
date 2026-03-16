#1.enumerate() basic
names=['zhan','aru','samal','kazyna','madina']
for i, name in enumerate(names):
    print(i,name)

#2.enumerate()-starting from 100
for i,name in enumerate(names,start=100):
    print(i,name)

#3.zip()-two lists
numb=[1,2,3]
let=['a','b','c']
for n,l in zip(numb,let):
    print(n,l)

#4.zip()-to create dictionary
d=dict(zip(numb,let))
print(d)

#5.tyoe checking and type conversion
v='10'
print(type(v))

n=int(v)
print(n+5)

f=float("3.14")
print(type(f))

s=str(25)
print(type(s))