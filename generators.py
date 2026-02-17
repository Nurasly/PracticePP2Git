def squares_up_to(n):
    for i in range(n + 1):
        yield i * i

for sq in squares_up_to(10):
    print(sq, end=' ')



def even_numbers_up_to(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input("Enter a number: "))
print(", ".join(map(str, even_numbers_up_to(n))))


def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = 50
print(list(divisible_by_3_and_4(n)))


def squares(a, b):
    for num in range(a, b + 1):
        yield num ** 2

start = 5
end = 12

print(f"Squares from {start} to {end}:")
for val in squares(start, end):
    print(val, end=" ")


def countdown_better(n):
    for i in range(n, -1, -1):
        yield i
print("Countdown:")
for num in countdown(8):
    print(num, end=" → ")
print("BOOM!")