from flask import jsonify

from db import InMemoryDB, InventoryDB
from models import Inventory, Item, ItemMetadata

class AppService:
    def __init__(self):
        self.db: InventoryDB = InMemoryDB()

    def create_inventory(self, name: str) -> Inventory:
        new_inventory = Inventory(name=name)
        return self.db.add_inventory(new_inventory)
    
    def get_inventory(self, id: int) -> Inventory:
        return self.db.get_inventory(id)
