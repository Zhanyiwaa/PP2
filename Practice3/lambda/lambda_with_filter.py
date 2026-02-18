#1
numbers=[1,2,3,4,5,6]
evens=list(filter(lambda x:x%2==0,numbers))
print(evens)

#2
ages=[12,17,18,21]
adults=list(filter(lambda age:age>=18,ages))
print(adults)

#3
words=["apple","hi","babay"]
long_words=list(filter(lambda w:len(w)>3,words))
print(long_words)

#4
numbers=[-5,3,-8,0,1]
positive=list(filter(lambda x:x>0,numbers))
print(positive)