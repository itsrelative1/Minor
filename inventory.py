class Inventory(object):
    """
    The inventory class containing the items for the player and the rooms
    """
    def __init__(self):
        """
        Inventory for each room and player
        """
        self.inventory = {}

    def delete(self, item_name):
        """
        Deletes the item from self.inventory dictionary
        """
        return self.inventory.pop(item_name)

    def add(self, item):
        """
        Adds items to the above dictionary with the name as key
        """
        self.inventory[item.name] = item

    def __str__(self):
        """
        Returns inventory as a string
        """
        tmp_inventory = ""

        for key, key_desc in self.inventory.items():
            tmp_inventory += f"{key}: {key_desc.description}\n"

        return tmp_inventory.strip()

