class Item(object):
    """
    Representation of an item in Adventure
    """
    def __init__(self, name, description, initial_location):
        """
        Initializes item attributes
        """
        self.name = name
        self.description = description
        self.initial_location = initial_location

    def __str__(self):
        return f"{self.name.upper()}: {self.description}"

