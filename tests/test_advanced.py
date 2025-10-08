"""Advanced edge-case tests for the time-based key-value store."""
import pytest
from database import Solution


def test_same_timestamp_last_write_wins():
    """Two sets at the same timestamp: the later write should win."""
    db = Solution()
    db.set("k", "v1", timestamp=10)
    db.set("k", "v2", timestamp=10)
    assert db.get("k", timestamp=10) == "v2"
    assert db.get_at("k", timestamp=10) == "v2"


def test_delete_then_set_same_timestamp_set_wins():
    """At the same timestamp, if a set happens after a delete, set should win (later op)."""
    db = Solution()
    db.set("k", "v1", timestamp=5)
    db.delete("k", timestamp=10)
    db.set("k", "v2", timestamp=10)  # later append at same ts
    assert db.get("k", timestamp=10) == "v2"
    assert db.get("k", timestamp=11) == "v2"


def test_set_then_delete_same_timestamp_delete_wins():
    """At the same timestamp, if delete is recorded after set, delete should win (later op)."""
    db = Solution()
    db.set("k", "v1", timestamp=5)
    db.set("k", "v2", timestamp=10)
    db.delete("k", timestamp=10)  # later append at same ts
    assert db.get("k", timestamp=10) is None
    assert db.get("k", timestamp=11) is None


def test_overlapping_ttls_choose_latest_valid():
    """Overlapping TTL windows: choose the latest set that is still valid at query time."""
    db = Solution()
    # v1 valid [10, 20)
    db.set("k", "v1", timestamp=10, ttl=10)
    # v2 valid [15, 30)
    db.set("k", "v2", timestamp=15, ttl=15)
    # At t=16, both valid; choose v2 (latest <= t)
    assert db.get("k", timestamp=16) == "v2"
    # After v1 expires, still v2
    assert db.get("k", timestamp=21) == "v2"


def test_ttl_boundary_half_open():
    """TTL window should be half-open [set_ts, set_ts+ttl): expired exactly at boundary."""
    db = Solution()
    db.set("k", "v", timestamp=100, ttl=5)  # valid 100..104
    assert db.get("k", timestamp=104) is None
    assert db.get("k", timestamp=103) == "v"


@pytest.mark.xfail(reason="Strict interpretation: ttl=0 means immediately expired; implementation may treat as no TTL.")
def test_ttl_zero_immediate_expiry():
    """If ttl=0, value should be expired immediately (strict semantics)."""
    db = Solution()
    db.set("k", "v", timestamp=50, ttl=0)
    assert db.get("k", timestamp=50) is None
    assert db.get("k", timestamp=51) is None


def test_large_timestamps_and_gaps():
    """Handle very large timestamps and sparse updates."""
    db = Solution()
    db.set("k", "early", timestamp=1)
    db.set("k", "late", timestamp=10_000_000)
    assert db.get("k", timestamp=9_999_999) == "early"
    assert db.get("k", timestamp=10_000_000) == "late"


def test_interleaved_keys_with_deletes_and_ttls():
    """Interleaved operations across keys with deletes and TTLs."""
    db = Solution()
    db.set("a", "a1", timestamp=1)
    db.set("b", "b1", timestamp=2, ttl=3)   # valid [2,5)
    db.set("a", "a2", timestamp=3)
    db.delete("a", timestamp=4)
    db.set("b", "b2", timestamp=5)
    # Check timeline
    assert db.get("a", timestamp=1) == "a1"
    assert db.get("a", timestamp=3) == "a2"
    assert db.get("a", timestamp=4) is None
    assert db.get("a", timestamp=6) is None
    assert db.get("b", timestamp=3) == "b1"
    assert db.get("b", timestamp=5) == "b2"  # b1 expired at 5
