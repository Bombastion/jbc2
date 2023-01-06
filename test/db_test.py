import pytest

from db import InMemoryDB
from models import Item, ItemMetadata


def test_add_item_metadata__requires_name():
    test_item = ItemMetadata(name="")

    subject = InMemoryDB()
    with pytest.raises(ValueError):
        subject.add_item_metadata(test_item)

def test_add_item_metadata():
    test_item = ItemMetadata(name="test")

    subject = InMemoryDB()

    result = subject.add_item_metadata(test_item)

    assert result.id == 0
    assert result.name == "test"
    assert len(subject.item_metadata) == 1


def test_add_item_metadata__increments_id():
    test_item = ItemMetadata(name="test")

    subject = InMemoryDB()

    subject.add_item_metadata(test_item)
    # Add a second entry to test IDs
    result = subject.add_item_metadata(test_item)

    assert result.id == 1
    assert result.name == "test"
    assert len(subject.item_metadata) == 2

def test_add_item__requires_valid_amount():
    test_item = Item(amount=-5, metadata_id=None, id=None)

    subject = InMemoryDB()

    with pytest.raises(ValueError) as ve:
        subject.add_item(test_item)

    assert "Item amount" in str(ve.value)

def test_add_item__requires_metadata_id():
    test_item = Item(amount=1, metadata_id=None, id=None)

    subject = InMemoryDB()

    with pytest.raises(ValueError) as ve:
        subject.add_item(test_item)

    assert "Invalid metadata_id" in str(ve.value)

def test_add_item__requires_matching_metadata():
    test_item = Item(amount=1, metadata_id=999, id=None)

    subject = InMemoryDB()

    with pytest.raises(ValueError) as ve:
        subject.add_item(test_item)

    assert "Invalid metadata_id" in str(ve.value)

def test_add_item():
    test_item = Item(amount=1, metadata_id=999, id=None)

    subject = InMemoryDB()
    subject.item_metadata[999] = None

    subject.add_item(test_item)
    result = subject.add_item(test_item)

    assert result.amount == 1
    assert result.metadata_id == 999
    assert result.id == 1
    assert len(subject.items) == 2

def test_get_item__none_when_no_id():
    subject = InMemoryDB()
    assert subject.get_item(99) is None 

def test_get_item():
    test_item = Item(amount=1, metadata_id=999, id=None)

    subject = InMemoryDB()
    subject.item_metadata[999] = None
    test_item = subject.add_item(test_item)
    result = subject.get_item(test_item.id)

    assert result == test_item
