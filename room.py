from inventory import Inventory


class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description):
        """
        Initializes a Room
        """
        self.id = id
        self.name = name
        self.description = description
        self.routes = {}
        self.room_inventory = Inventory()
        self.explored = False

    def add_route(self, direction, room):
        """
        Adds a given direction and the connected room to our room object
        """
        if direction not in self.routes:

            self.routes[direction] = []

        self.routes[direction].append(room)

    def is_connected(self, direction):
        """
        Checks whether the given direction has a connection from a room
        Returns a boolean.
        """
        if direction in self.routes:
            return True

        return False

    def show(self):
        """
        Shows the desired attributes of the room
        """
        # Returns inventory as well if not empty
        if self.room_inventory.inventory != {}:
            return f"{self.description}\n{self.room_inventory}"

        # Only returns description if empty
        else:
            return f"{self.description}"

    def force_player(self):
        return self.routes['FORCED']

    def __str__(self):
        """
        Returns string description of room
        """
        if self.explored == True:

            # Returns only name if it has been explored
            return f"{self.name}"

        # If not return full description and possibly the inventory as well
        else:
            self.explored = True
            return self.show()

