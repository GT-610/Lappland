import unittest
from container import Container

class TestContainer(unittest.TestCase):

    def test_createContainer(self):
        container_instance = Container()

        # Test if createContainer adds a container to list.yaml
        container_instance.createContainer("first", "ubuntu", "23.04")
        # Add more tests based on your requirements

if __name__ == '__main__':
    unittest.main()
