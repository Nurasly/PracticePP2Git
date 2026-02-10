class Animal:
    def speak(self):
        return "Generic animal sound"

class Dog(Animal):
    # This method overrides the speak() method in the Animal class
    def speak(self):
        return "Woof!"

# Usage
animal_instance = Animal()
dog_instance = Dog()

print(animal_instance.speak()) # Output: Generic animal sound
print(dog_instance.speak())    # Output: Woof! 
