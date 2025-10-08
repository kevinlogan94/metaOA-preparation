"""Basic set and get tests for the time-based key-value store."""
from database import Solution


def test_set_and_get_immediately():
    """Set a value and immediately get it."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    assert db.get("key1", timestamp=1) == "value1"


def test_set_multiple_keys():
    """Set multiple different keys, get each value."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    db.set("key2", "value2", timestamp=2)
    db.set("key3", "value3", timestamp=3)
    
    assert db.get("key1", timestamp=3) == "value1"
    assert db.get("key2", timestamp=3) == "value2"
    assert db.get("key3", timestamp=3) == "value3"


def test_overwrite_key():
    """Overwrite a key and check retrieval gives the latest value."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    db.set("key1", "value2", timestamp=2)
    
    assert db.get("key1", timestamp=2) == "value2"


def test_get_nonexistent_key():
    """Get a key that does not exist."""
    db = Solution()
    assert db.get("nonexistent", timestamp=1) is None


def test_overwrite_multiple_times():
    """Overwrite a key multiple times and verify the latest value."""
    db = Solution()
    db.set("key1", "v1", timestamp=1)
    db.set("key1", "v2", timestamp=2)
    db.set("key1", "v3", timestamp=3)
    db.set("key1", "v4", timestamp=4)
    
    assert db.get("key1", timestamp=4) == "v4"
