class Dog:
    species = 'Canis familiaris' # Class variable shared by all instances
    count = 0 # Another class variable to track instances

    def __init__(self, name):
        self.name = name       # Instance variable unique to each instance
        Dog.count += 1         # Correctly incrementing the class variable

d = Dog('Fido')
e = Dog('Buddy')

print(d.species)     # Output: Canis familiaris
print(e.species)     # Output: Canis familiaris
print(Dog.species)   # Output: Canis familiaris

print(Dog.count)     # Output: 2
