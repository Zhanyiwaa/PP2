#1.square generator
def square_generator(n):
    for i in range(n+1):
        yield i*i

#2.even numbers
def even_numbers(n):
    for i in range(n+1):
        if i%2==0:
            yield i

#3.divisible by 3 and 4
def divisible(n):
    for i in range(n+1):
        if i%3==0 and i%4==0:
            yield i


#4.squares
def squares(a,b):
    for i in range(a,b+1):
        yield i*i

#5.countdown
def countdown(n):
    while n>=0:
        yield n
        n-=1




# Testing section
if __name__ == "__main__":
    print("Squares up to 5:")
    for num in square_generator(5):
        print(num)

    n = int(input("Enter n for even numbers: "))
    print(",".join(str(x) for x in even_numbers(n)))

    print("Divisible by 3 and 4 up to 100:")
    for num in divisible(100):
        print(num)

    print("Squares from 3 to 7:")
    for num in squares(3, 7):
        print(num)

    print("Countdown from 5:")
    for num in countdown(5):
        print(num)
