"""Versioning and point-in-time query tests for the time-based key-value store."""
from database import Solution


def test_get_at_previous_timestamp():
    """Set a key, update it, and query at the previous timestamp returns old value."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    db.set("key1", "value2", timestamp=5)
    
    # Query at timestamp 3 should return value1
    assert db.get_at("key1", timestamp=3) == "value1"
    # Query at timestamp 5 should return value2
    assert db.get_at("key1", timestamp=5) == "value2"


def test_sequential_updates_versioning():
    """Make several sequential updates and ensure queries at each version return correct value."""
    db = Solution()
    db.set("key1", "v1", timestamp=1)
    db.set("key1", "v2", timestamp=3)
    db.set("key1", "v3", timestamp=5)
    db.set("key1", "v4", timestamp=7)
    
    assert db.get_at("key1", timestamp=1) == "v1"
    assert db.get_at("key1", timestamp=2) == "v1"
    assert db.get_at("key1", timestamp=3) == "v2"
    assert db.get_at("key1", timestamp=4) == "v2"
    assert db.get_at("key1", timestamp=5) == "v3"
    assert db.get_at("key1", timestamp=6) == "v3"
    assert db.get_at("key1", timestamp=7) == "v4"


def test_query_before_key_set():
    """Query a key before it was ever set; expect None."""
    db = Solution()
    db.set("key1", "value1", timestamp=5)
    
    assert db.get_at("key1", timestamp=3) is None


def test_query_with_ttl_in_past():
    """Query a key's value that had a valid TTL in the past."""
    db = Solution()
    db.set("key1", "value1", timestamp=1, ttl=10)  # Valid from 1 to 10
    
    # Query at timestamp 5 (within TTL window)
    assert db.get_at("key1", timestamp=5) == "value1"
    # Query at timestamp 11 (expired)
    assert db.get_at("key1", timestamp=11) is None


def test_multiple_keys_independent_histories():
    """Multiple keys with independent version histories."""
    db = Solution()
    db.set("key1", "v1", timestamp=1)
    db.set("key2", "v2", timestamp=2)
    db.set("key1", "v1_updated", timestamp=3)
    db.set("key2", "v2_updated", timestamp=4)
    
    # Query key1 at different times
    assert db.get_at("key1", timestamp=2) == "v1"
    assert db.get_at("key1", timestamp=3) == "v1_updated"
    
    # Query key2 at different times
    assert db.get_at("key2", timestamp=3) == "v2"
    assert db.get_at("key2", timestamp=4) == "v2_updated"


def test_query_between_two_sets():
    """Query between two sets and verify which value is returned."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    db.set("key1", "value2", timestamp=10)
    
    # Query at timestamp 5 (between the two sets)
    assert db.get_at("key1", timestamp=5) == "value1"


def test_query_with_ttl_expired_at_timestamp():
    """Query with TTL expired at a specific timestamp to confirm None."""
    db = Solution()
    db.set("key1", "value1", timestamp=5, ttl=10)  # Expires at 15
    
    # Query at timestamp 15 (exactly at expiration)
    assert db.get_at("key1", timestamp=15) is None
    # Query at timestamp 14 (just before expiration)
    assert db.get_at("key1", timestamp=14) == "value1"


def test_update_with_different_ttls():
    """Update a key with different TTLs; confirm correct behavior at each timestamp."""
    db = Solution()
    db.set("key1", "v1", timestamp=1, ttl=5)   # Valid 1-5
    db.set("key1", "v2", timestamp=3, ttl=10)  # Valid 3-12
    
    # At timestamp 2, v1 is valid
    assert db.get_at("key1", timestamp=2) == "v1"
    # At timestamp 4, v2 is valid
    assert db.get_at("key1", timestamp=4) == "v2"
    # At timestamp 6, v1 would have expired, but v2 is still valid
    assert db.get_at("key1", timestamp=6) == "v2"
    # At timestamp 13, v2 has expired
    assert db.get_at("key1", timestamp=13) is None
