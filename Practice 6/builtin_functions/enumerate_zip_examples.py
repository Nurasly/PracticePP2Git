names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

# zip: Combine lists
for name, score in zip(names, scores):
    print(f"{name} got a {score}")

# enumerate: Get index
for index, name in enumerate(names, start=1):
    print(f"Rank {index}: {name}")