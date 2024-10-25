import unittest

from A7.A7 import Person
from A7.A7 import PersonDictionary

class PersonDictionaryTest(unittest.TestCase):

    def setUp(self):
        # Set up some mock data for testing
        self.p1 = Person("John", "Doe", 30)
        self.p2 = Person("Jane", "Doe", 25)
        self.p3 = Person("Rick", "Astley", 57)
        
        # Create a PersonDictionary instance and manually add people to the list
        self.person_dict = PersonDictionary()
        self.person_dict.people = [self.p1, self.p2, self.p3]

    def test_GetByFirst(self):
        pass

    def test_GetByLast(self):
        pass

    def test_GetByAge(self):
        pass

    def test_GetOldest(self):
        pass

    def test_GetYoungest(self):
        pass

    def test_StartIteration(self):
        pass

    def test_isDone(self):
        pass
    
    def test_GetNext(self):
        pass

if __name__ == "__main__":
    unittest.main()