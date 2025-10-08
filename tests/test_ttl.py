"""TTL (time-to-live) tests for the time-based key-value store."""
from database import Solution


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
