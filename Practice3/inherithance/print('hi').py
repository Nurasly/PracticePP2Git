a = int(input())
b = int(input())
k = int(input())
sum = 0
for i in range(a, b):
    if i%k == 0:
        sum += 1
print(sum)
