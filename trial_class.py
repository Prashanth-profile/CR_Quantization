class Person:
    def __init__(self, data_list):
        self.data = data_list

# Example data list
data1 = ["Alice", 25]
data2 = ["Bob", 30]

# Create instances of the Person class using data lists
person1 = Person(data1)
person2 = Person(data2)

# Print instance attributes
print("Person 1 Data:", person1.data)
print("Person 2 Data:", person2.data)
