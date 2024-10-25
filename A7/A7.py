class Person:
    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

class PersonDictionary:
    def __init__(self):
        self.people = []

    def ReadFile(self, file: str) -> bool:
        # To be implemented
        pass

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