import os

class Person:
    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

class PersonDictionary:
    def __init__(self):
        self.people = []

    def ReadFile(self, filename: str = None) -> bool:
        try:
            # Get the filename from the user if none is provided
            if not filename:
                filename = input("Enter the name of the file to read: ")

            # This will look for the text file inside of the A7 folder
            file_path = os.path.join("A7", filename)

            # Open the file and read in the names
            with open(file_path, 'r') as file:
                for line in file:
                    # Split the line by spaces (First Name, Last Name, Age)
                    first_name, last_name, age = line.strip().split()
                    # Create a new Person object and add to the list
                    person = Person(first_name, last_name, int(age))
                    print(f"Read in {person.first_name} {person.last_name} ({person.age})")
                    self.people.append(person)

            print(f"Successfully read {len(self.people)} people from the file.")
            return True
        
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return False
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def GetByFirst(self, first_name: str) -> Person:
        # To be implemented
        pass

    def GetByLast(self, last_name: str) -> Person:
        # To be implemented
        pass

    def GetByAge(self, age: int) -> Person:
        # To be implemented
        pass

    def GetAge(self, first_name: str, last_name: str) -> int:
        # To be implemented
        pass

    def GetOldest(self) -> Person:
        # To be implemented
        pass

    def GetYoungest(self) -> Person:
        # To be implemented
        pass

    def StartIteration(self) -> None:
        # To be implemented
        pass

    def IsDone(self) -> bool:
        # To be implemented
        pass

    def GetNext(self) -> Person:
        # To be implemented
        pass

# Driver code
if __name__ == "__main__":
    person_dict = PersonDictionary()
    person_dict.ReadFile()

