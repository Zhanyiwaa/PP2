#1
numbers=[1,2,3,4,]
result=list(map(lambda x:x*2,numbers))
print(result)

#2
names=["anna","mark","greg"]
upper_names=list(map(lambda name:name.upper(),names))
print(upper_names)

#3
prices=[100,200,300]
discounted=list(map(lambda d:d*0.9,prices))
print(discounted)

#4
words=["apple","banana"]
lengths=list(map(lambda w:len(w),words))
print(lengths)