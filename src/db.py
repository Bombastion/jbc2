from abc import ABC, abstractmethod
from copy import deepcopy
import typing

from models import Inventory, Item, ItemMetadata

class InventoryDB(ABC):
    @abstractmethod
    def add_item(self, item: Item) -> Item:
        """ Adds an item to the DB and hydrates its ID
        """
        pass

    @abstractmethod
    def get_item(self, id: int) -> Item:
        """ Finds an item by ID
        """
        pass

    @abstractmethod
    def add_item_metadata(self, metadata: ItemMetadata) -> ItemMetadata:
        """ Adds an item metaedata to the DB and hydrates its ID
        """
        pass

    @abstractmethod
    def get_item_metadata(self, id: int) -> ItemMetadata:
        """ Finds an ItemMetadata by ID
        """
        pass

    @abstractmethod
    def add_inventory(self, inventory: Inventory) -> Inventory:
        """ Adds an inventory to the DB and hydrates its ID
        """
        pass

    @abstractmethod
    def get_inventory(self, id: int) -> Inventory:
        """ Finds an inventory by ID
        """
        pass

class InMemoryDB(InventoryDB):
    def __init__(self):
        self.items: typing.Dict[int, Item] = {}
        self.item_metadata: typing.Dict[int, ItemMetadata] = {}
        self.inventories: typing.Dict[int, Inventory] = {}

    def _get_next_id(self, list: typing.List) -> int:
        """ Gets the next ID for the given list, starting at 0
        """
        return max(list, default=-1) + 1

    def _validate_item(self, item: Item)-> None:
        if item.amount < 0:
            raise ValueError(f"Item amount {item.amount} cannot be negative")
        if item.metadata_id is None or not self.get_item_metadata(item.metadata_id):
            raise ValueError(f"Cannot add item with invalid metadata_id {item.metadata_id}")
        if item.inventory_id is None or not self.get_inventory(item.inventory_id):
            raise ValueError(f"Cannot add item with invalid inventory_id {item.inventory_id}")


    def _add_db_item(self, object: typing.Any, validate_method: typing.Callable, collection: typing.Dict[int, typing.Any], expected_type: type[object]) -> typing.Any:
        db_object = deepcopy(object)
        validate_method(db_object)
        if not isinstance(object, expected_type):
            raise ValueError(f"Cannot insert {object} with expected type {expected_type}")
        if db_object.id is None:
            db_object.id = self._get_next_id(collection.keys())
        
        collection[db_object.id] = db_object
        return db_object

    def add_item(self, item: Item) -> Item:
        """ Adds an item to the DB and hydrates its ID if empty
        returns: A deep copy of the updated item
        """
        return self._add_db_item(item, self._validate_item, self.items, Item)

    def get_item(self, id: int) -> Item:
        return self.items.get(id)

    def _validate_item_metadata(self, metadata: ItemMetadata)-> None:
        if not metadata.name:
            raise ValueError(f"Item name cannot be empty: {metadata.name}")

    def add_item_metadata(self, metadata: ItemMetadata) -> ItemMetadata:
        """ Adds an item metadata to the DB and hydrates its ID if empty
        returns: A deep copy of the updated metadata
        """
        return self._add_db_item(metadata, self._validate_item_metadata, self.item_metadata, ItemMetadata)

    def get_item_metadata(self, id: int) -> ItemMetadata:
        return self.item_metadata.get(id)

    def _validate_inventory(self, inventory: Inventory) -> None:
        if not inventory.name:
            raise ValueError(f"Inventory name cannot be empty: {inventory.name}")
    
    def add_inventory(self, inventory: Inventory) -> Inventory:
        return self._add_db_item(inventory, self._validate_inventory, self.inventories, Inventory)

    def get_inventory(self, id: int) -> Inventory:
        return self.inventories.get(id)