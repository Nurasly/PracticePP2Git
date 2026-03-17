with open("data.txt", "r") as f:
    content = f.readlines()
    print([line.strip() for line in content])