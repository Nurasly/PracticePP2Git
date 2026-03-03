import re

pattern = r"^ab*$"
text = "abbb"
print(bool(re.match(pattern, text)))





pattern = r"^ab{2,3}$"
text = "abb"
print(bool(re.match(pattern, text)))





text = "hello_world test_string Example"
pattern = r"[a-z]+_[a-z]+"
print(re.findall(pattern, text))



text = "Hello World ABC Test"
pattern = r"[A-Z][a-z]+"
print(re.findall(pattern, text))




pattern = r"^a.*b$"
text = "axxxb"
print(bool(re.match(pattern, text)))




text = "Hello, world. Python is fun"
result = re.sub(r"[ ,.]", ":", text)
print(result)



def snake_to_camel(text):
    parts = text.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])
print(snake_to_camel("hello_world_test"))




text = "HelloWorldTest"
result = re.split(r"(?=[A-Z])", text)
print(result)





text = "HelloWorldTest"
result = re.sub(r"(?<!^)(?=[A-Z])", " ", text)
print(result)




def camel_to_snake(text):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()
print(camel_to_snake("helloWorldTest"))