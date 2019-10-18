from room import Room
from item import Item
from inventory import Inventory
import sys


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """

    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """
        self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
        self.items = self.load_items(f"data/{game}Items.txt")
        self.synonyms = self.load_synonyms(f"data/SmallSynonyms.txt")
        self.current_room = self.rooms[1]
        self.player_inventory = Inventory()
        self.rooms[1].explored = True

    def load_synonyms(self, filename):
        """
        Load synonyms into dictionary as abbreviation : command
        """
        synonyms = {}

        with open(filename, "r") as f:

            # Iterates through the lines in synonyms textfile
            for line in f:

                if not line == "\n":

                    # File lines are formatted as Abbreviation=Commmand
                    abbreviation, full_comm = line.split("=")

                    # Write dictionary with abbreciation as key
                    synonyms[abbreviation] = full_comm.strip()

        return synonyms

    def load_rooms(self, filename):
        """
        Load rooms from filename and returns a dictionary of 'id' : Room objects
        """
        # First we parse all the data we need to create the rooms with
        # All parsed lines of data are saved to rooms_data
        rooms_data = []

        with open(filename, "r") as f:

            room_data = []

            for line in f:

                # When there is no blank newline it means there's still data
                if not line == "\n":
                    room_data.append(line.strip())

                # A blank newline signals all data of a single room is parsed
                else:
                    rooms_data.append(room_data)
                    room_data = []

        # Append a final time, because the files do not end on a blank newline
        rooms_data.append(room_data)

        # Create room objects for each set of data we just parsed
        rooms = {}
        for room_data in rooms_data:

            id = int(room_data[0])
            name = room_data[1]
            description = room_data[2]

            # Initialize a room object and put it in a dictionary with its id as key
            room = Room(id, name, description)
            rooms[id] = room

        # Add routes to each room we've created
        for room_data in rooms_data:
            id = int(room_data[0])

            # We split to connections into a direction and a room_id.
            connections = room_data[4:]
            connections = [connection.split() for connection in connections]

            # Here we get the current room object that we'll add routes to.
            room = rooms[id]

            for connection, target_room_id in connections:

                # Adds routes to room object
                room.add_route(connection, target_room_id)

        return rooms

    def load_items(self, filename):
        """
        Load items from filename.
        """
        # Same as with load_rooms, parse the data and put them into items_data
        items_data = []

        with open(filename, 'r') as f:

            item_data = []

            for line in f:

                # If there is data append to items_data
                if not line == "\n":
                    item_data.append(line.strip())

                # Else append the list to item_data
                else:
                    items_data.append(item_data)
                    item_data = []

            # Append a final time, because the files do not end on a blank newline
            items_data.append(item_data)

            # Dictionary for all item objects
            items = {}

            for item_data in items_data:

                item_name = item_data[0]
                item_description = item_data[1]
                item_location = int(item_data[2])

                # Creates item object with item_data
                item = Item(item_name, item_description, item_location)

                # Puts the item in dictionary with item_name as key
                items[item_name] = item

                # Adds items to rooms
                self.rooms[item_location].room_inventory.add(item)

        return items

    def game_over(self):
        """
        Check if the game is over and returns a boolean
        """
        # If roomname is victory, return true
        if self.current_room.name == "Victory":
            return True

        # If room_id is 0 and roomname not Victory, lost
        elif self.current_room.id == '0':
            return True

        return False

    def move(self, direction):
        """
        Moves to a different room in the specified direction
        """
        # Retrieves the ID of the connected room when direction is given
        self.connected_list = self.current_room.routes[direction]

        for connection in self.connected_list:

            movement = connection.split("/")

            if len(movement) == 2:
                f_move = int(movement[0])
                f_item = movement[1]

                if f_item in self.player_inventory.inventory:

                    self.current_room = self.rooms[f_move]
                    break
                else:
                    continue

            elif len(movement) == 1:
                f_move = int(movement[0])
                self.current_room = self.rooms[f_move]

    def drop(self, item_name, room_inv, player_inv):
        """
        Drops items to current room
        """
        # Checks if item in player inventory
        if item_name in player_inv.inventory:

            # Delete item from player inventory
            player_inv.delete(item_name)

            # Add item to room inventory
            room_inv.add(self.items[item_name])

            # Print item that is dropped
            print(f"{item_name} dropped.")

        else:
            print("No such item.")

    def take(self, item_name, room_inv, player_inv):
        """
        Takes item from room_inv and puts it in player_inv
        """
        # Checks if item_name is in the room_inv inventory
        if item_name in room_inv.inventory:

            # Deletes the item from room_inv
            room_inv.delete(item_name)

            # Adds item to player inventory
            player_inv.add(self.items[item_name])

            # Standard print message
            print(f"{item_name} taken.")

        else:
            print("No such item.")

    def inventory_check(self):
        """
        Looks inside the inventory of the player
        """
        # Checks if inventory is empty
        if self.player_inventory.inventory != {}:

            # returns player inventory
            return(self.player_inventory)

        else:
            return f"Your inventory is empty."

    def input_command(self):
        """
        Converts command into something usable
        """
        com_input = input("> ").upper()
        split_input = com_input.split(" ")

        # If 2 commands entered, second one is item
        if len(split_input) == 2:
            tmp_command = split_input[0]
            tmp_item = split_input[1]

        # If only one command, return empty string for item
        elif len(split_input) == 1:
            tmp_command = split_input[0]
            tmp_item = ""

        if tmp_command in self.synonyms:
            tmp_command = self.synonyms[tmp_command]

        return tmp_command, tmp_item

    def help(self):
        print(f"You can move by typing directions such as EAST/WEST/IN/OUT.\n"
              "QUIT quits the game.\n"
              "HELP prints instructions for the game.\n"
              "INVENTORY lists the item in your inventory.\n"
              "LOOK lists the complete description of the room and its contents.\n"
              "TAKE <item> take item from the room.\n"
              "DROP <item> drop item from your inventory.")

    def quit(self):
        """
        Quits game with exitcode 0
        """
        print("Thanks for playing!")
        exit(0)

    def look(self):
        """
        Shows the room description and inventory if any
        """
        print(self.current_room.show())

    def inventory(self):
        """
        Shows the player inventory if not empty
        """
        print(self.inventory_check())

    def play(self):
        """
        Play an Adventure game
        """
        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n")
        print(f"{self.current_room.description}")

        # Prompt the user for commands until they've won the game.
        while not self.game_over():
            command, command_item = self.input_command()

            # Check if the command is a movement or not.
            if self.current_room.is_connected(command):

                # Move to new room
                self.move(command)

                # Prints proper description of location
                print(self.current_room)

                while "FORCED" in self.current_room.routes:

                    if self.current_room.routes["FORCED"][0] != "0":
                        self.move("FORCED")
                        print(self.current_room)

                    else:
                        self.current_room.id = "0"
                        break

            # Getattr looks at Adventure() attributes and methods and calls the right one
            elif command in ["HELP", "QUIT", "LOOK", "INVENTORY"]:
                getattr(self, command.lower())()

            elif command in ["TAKE", "DROP"]:
                getattr(self, command.lower())(command_item, self.current_room.room_inventory, self.player_inventory)

            else:
                print("Invalid command.")


if __name__ == "__main__":

    # Ensures proper usage: python adventure.py name
    if len(sys.argv) == 2:
        gametype = sys.argv[1]
        adventure = Adventure(gametype)
        adventure.play()

    # Print usage if not valid
    else:
        print("Usage: python adventure.py NAME")