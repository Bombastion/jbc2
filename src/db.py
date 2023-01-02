from abc import ABC, abstractmethod
from copy import deepcopy
import typing

from models import Item, ItemMetadata

class InventoryDB(ABC):
    @abstractmethod
    def add_item(self, item: Item) -> Item:
        """ Adds an item to the DB and hydrates its ID
        """
        pass

    @abstractmethod
    def add_item_metadata(self, metadata: ItemMetadata) -> ItemMetadata:
        """ Adds an item metaedata to the DB and hydrates its ID
        """
        pass

class InMemoryDB(InventoryDB):
    def __init__(self):
        self.items: typing.Dict[int, Item] = {}
        self.item_metadata: typing.Dict[int, ItemMetadata] = {}

    def _validate_item(self, item: Item)-> None:
        if item.amount < 0:
            raise ValueError(f"Item amount {item.amount} cannot be negative")
        if item.metadata_id is None or item.metadata_id not in self.item_metadata.keys():
            raise ValueError(f"Invalid metadata_id {item.metadata_id}")

    def add_item(self, item: Item) -> Item:
        """ Adds an item to the DB and hydrates its ID if empty
        returns: A deep copy of the updated item
        """
        db_item = deepcopy(item)
        self._validate_item(db_item)
        if db_item.id is None:
            db_item.id = max(self.items.keys(), deault=0)

        self.items[db_item.id] = db_item
        return db_item

    def _validate_item_metadata(self, metadata: ItemMetadata)-> None:
        if not metadata.name:
            raise ValueError(f"Item name cannot be empty: {metadata.name}")

    def add_item_metadata(self, metadata: ItemMetadata) -> ItemMetadata:
        """ Adds an item metadata to the DB and hydrates its ID if empty
        returns: A deep copy of the updated metadata
        """
        db_object = deepcopy(metadata)
        self._validate_item_metadata(db_object)
        if db_object.id is None:
            db_object.id = max(self.item_metadata.keys(), default=0)

        self.items[db_object.id] = db_object
        return db_object