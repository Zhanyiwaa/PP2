#1
class Calculator:
    def add(self,a,b):
        return a+b
    
calc=Calculator()
print(calc.add(2,3))

#2
class Counter:
    def __init__(self):
        self.count=0

    def increment(self):
        self.count+=1

c=Counter()
c.increment()
print(c.count)

#3
class BankAccount():
    def __init__(self,balance):
        self.balance=balance

    def deposit(self,amount):
        self.balance+=amount

acc=BankAccount(500)
acc.deposit(200)
print(acc.balance)

#4
class Rectangle:
    def area(self,width,length):
        return width*length
    
r=Rectangle()
print(r.area(4,5))

