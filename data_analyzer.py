# Variables

name = "Mustafa"           # Strinng
age = 34                   # Integer
fruits = ["apple", "mango", "bluebery"]  # List
student = {"name": name, "age": age, "grades": [90, 99, 92]}  # Dictionary

# Data structures
numbers_list = [1, 2, 3, 4]
numbers_tuple = (5, 6, 7, 8)
person = {"first_name": "Mustafa", "last_name": "Ansari", "age": 34}

# String to int casting
age_str = str(age)  
age_int = int(age_str)

if __name__ == "__main__":
    # Variables
    print("Name:", name)
    print("Age:", age)
    print("Fruits:", fruits)
    print("Student info:", student)
    
    # Conditionals
    if age_int < 13:
        print("You are a child.")
    elif 13 <= age_int < 20:
        print("You are a teenager.")
    else:
        print("You are an adult.")
    
    # For Loop
    print("\nFor loop example:")
    for fruit in fruits:
        print("Fruit:", fruit)

    # While loop example
    counter = 0
    while counter < 3:
        print("Counter:", counter)
        counter += 1

    # Data structures
    print("List:", numbers_list)
    print("Tuple:", numbers_tuple)
    print("Dictionary:", person)

    # Built-in functions
    for index, fruit in enumerate(fruits):
        print(f"{index+1}: {fruit}")
    
    for i in range(3):
        print("Range number:", i)
    
    print("ID of 'name' variable:", id(name))

    # Import from utils.py
    from utils import greet
    print(greet(name))
