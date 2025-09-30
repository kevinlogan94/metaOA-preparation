import pytest
from database import Solution


# ============================================================================
# BASIC SET AND GET TESTS
# ============================================================================

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


# ============================================================================
# TTL (TIME-TO-LIVE) TESTS
# ============================================================================

def test_ttl_before_expiration():
    """Set a key with TTL and get value before it expires."""
    db = Solution()
    db.set("key1", "value1", timestamp=1, ttl=10)
    
    # Query at timestamp 5 (within TTL)
    assert db.get("key1", timestamp=5) == "value1"


def test_ttl_after_expiration():
    """Set a key with TTL and get nothing after it expires."""
    db = Solution()
    db.set("key1", "value1", timestamp=1, ttl=10)
    
    # Query at timestamp 11 (TTL expired at timestamp 11)
    assert db.get("key1", timestamp=11) is None
    # Query at timestamp 12 (after expiration)
    assert db.get("key1", timestamp=12) is None


def test_key_without_ttl_persists():
    """Set a key without TTL and verify it persists."""
    db = Solution()
    db.set("key1", "value1", timestamp=1)
    
    # Query far in the future
    assert db.get("key1", timestamp=1000) == "value1"


def test_mixed_ttl_and_no_ttl():
    """Mix keys with and without TTL and confirm only those with TTL expire."""
    db = Solution()
    db.set("key1", "value1", timestamp=1, ttl=10)  # Expires at 11
    db.set("key2", "value2", timestamp=1)          # No TTL
    
    # At timestamp 15, key1 expired, key2 still valid
    assert db.get("key1", timestamp=15) is None
    assert db.get("key2", timestamp=15) == "value2"


def test_overwrite_with_new_ttl():
    """Overwrite a key with a new TTL and check expiration updates."""
    db = Solution()
    db.set("key1", "value1", timestamp=1, ttl=5)   # Expires at 6
    db.set("key1", "value2", timestamp=3, ttl=10)  # Expires at 13
    
    # At timestamp 7, old TTL would have expired, but new TTL is active
    assert db.get("key1", timestamp=7) == "value2"
    # At timestamp 13, new TTL expires
    assert db.get("key1", timestamp=13) is None


def test_remove_ttl_by_overwriting():
    """Remove TTL by overwriting key without TTL and ensure it doesn't expire."""
    db = Solution()
    db.set("key1", "value1", timestamp=1, ttl=10)  # Expires at 11
    db.set("key1", "value2", timestamp=5)          # No TTL
    
    # At timestamp 15, should still be valid (no TTL)
    assert db.get("key1", timestamp=15) == "value2"


def test_overwrite_expired_key():
    """Overwrite a key that has expired and verify new value is present."""
    db = Solution()
    db.set("key1", "value1", timestamp=1, ttl=5)   # Expires at 6
    db.set("key1", "value2", timestamp=10)         # After expiration
    
    # At timestamp 10, new value should be present
    assert db.get("key1", timestamp=10) == "value2"


# ============================================================================
# VERSIONING / POINT-IN-TIME QUERY TESTS
# ============================================================================

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


# ============================================================================
# DELETE TESTS
# ============================================================================

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

