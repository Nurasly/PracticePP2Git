from functools import reduce

nums = [1, 2, 3, 4, 5]

# map: square them
squared = list(map(lambda x: x**2, nums))

# filter: keep evens
evens = list(filter(lambda x: x % 2 == 0, nums))

# reduce: sum them up
total = reduce(lambda x, y: x + y, nums)