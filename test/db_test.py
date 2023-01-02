import pytest

from db import InMemoryDB
from models import ItemMetadata


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
