class Solution:
    """
    Time-based key-value store with TTL and versioning support.
    
    Features:
    - set(key, value, timestamp, ttl=None): Store a value with optional TTL
    - get(key, timestamp): Get the current value at a timestamp
    - get_at(key, timestamp): Get the value at a specific point in time (versioning)
    - delete(key, timestamp): Delete a key at a timestamp
    """
    
    def __init__(self):
        # TODO: Implement data structure to store key-value pairs with timestamps and TTL
        pass
    
    def set(self, key: str, value: str, timestamp: int, ttl: int = None) -> None:
        """
        Set a key-value pair at a given timestamp with optional TTL.
        
        Args:
            key: The key to set
            value: The value to store
            timestamp: When this operation occurs
            ttl: Time-to-live in seconds (None means no expiration)
        """
        # TODO: Implement
        pass
    
    def get(self, key: str, timestamp: int) -> str:
        """
        Get the current value of a key at the given timestamp.
        
        Args:
            key: The key to retrieve
            timestamp: The current time
            
        Returns:
            The value if key exists and hasn't expired, None otherwise
        """
        # TODO: Implement
        return None
    
    def get_at(self, key: str, timestamp: int) -> str:
        """
        Get the value of a key as it was at a specific point in time.
        This supports versioning/time-travel queries.
        
        Args:
            key: The key to retrieve
            timestamp: The point in time to query
            
        Returns:
            The value at that timestamp if it existed and was valid, None otherwise
        """
        # TODO: Implement
        return None
    
    def delete(self, key: str, timestamp: int) -> None:
        """
        Delete a key at the given timestamp.
        
        Args:
            key: The key to delete
            timestamp: When this operation occurs
        """
        # TODO: Implement
        pass
