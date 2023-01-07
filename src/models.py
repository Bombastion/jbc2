from dataclasses import dataclass

@dataclass
class Item:
    amount: int
    metadata_id: int
    inventory_id: int
    id: int = None # To be automatically populated by the db
    

@dataclass
class ItemMetadata:
    name: str
    id: int = None # To be automatically populated by the db


@dataclass
class Inventory:
    name: str
    id: int = None # To be automatically populated by the db
