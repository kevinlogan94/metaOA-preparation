"""Delete operation tests for the time-based key-value store."""
from database import Solution


def test_delete_existing_key():
    """Delete an existing key and check it's gone."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    db.delete("key1", timestamp=5)
    
    assert db.get("key1", timestamp=6) is None


def test_delete_nonexistent_key():
    """Delete a non-existent key and ensure no error."""
    db = Solution()
    # Should not raise an error
    db.delete("nonexistent", timestamp=1)
    assert db.get("nonexistent", timestamp=2) is None


def test_query_before_and_after_delete():
    """Query a key before and after delete to check timeline integrity."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    db.delete("key1", timestamp=5)
    
    # Query before delete
    assert db.get_at("key1", timestamp=3) == "value1"
    # Query at delete time
    assert db.get_at("key1", timestamp=5) is None
    # Query after delete
    assert db.get_at("key1", timestamp=7) is None


def test_delete_then_set_again():
    """Delete then set a key again; confirm re-setting works after deletion."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    db.delete("key1", timestamp=5)
    db.set("key1", "value2", timestamp=10)
    
    # Before delete
    assert db.get_at("key1", timestamp=3) == "value1"
    # After delete, before re-set
    assert db.get_at("key1", timestamp=7) is None
    # After re-set
    assert db.get_at("key1", timestamp=10) == "value2"


def test_delete_same_key_multiple_times():
    """Delete the same key multiple times; confirm idempotence."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    db.delete("key1", timestamp=5)
    db.delete("key1", timestamp=6)
    db.delete("key1", timestamp=7)
    
    assert db.get("key1", timestamp=10) is None


def test_multiple_sets_and_deletes():
    """Multiple sets and deletes; verify correct values at each timeline interval."""
    db = Solution()
    db.set("key1", "v1", timestamp=1)
    db.set("key1", "v2", timestamp=3)
    db.delete("key1", timestamp=5)
    db.set("key1", "v3", timestamp=7)
    db.delete("key1", timestamp=9)
    
    assert db.get_at("key1", timestamp=2) == "v1"
    assert db.get_at("key1", timestamp=4) == "v2"
    assert db.get_at("key1", timestamp=6) is None
    assert db.get_at("key1", timestamp=8) == "v3"
    assert db.get_at("key1", timestamp=10) is None
