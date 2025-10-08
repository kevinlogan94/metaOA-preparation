import time
from collections import defaultdict
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
        self.data = defaultdict(list)
        pass
    
    def set(self, key: str, value: str, timestamp: int, ttl: int = None) -> dict:
        """
        Set a key-value pair at a given timestamp with optional TTL.
        
        Args:
            key: The key to set
            value: The value to store
            timestamp: When this operation occurs
            ttl: Time-to-live in seconds (None means no expiration)
        """
        self.data[key].append({"timestamp": timestamp, "value": value, "ttl": ttl, "deleted": False})
        return self.data[key]
    
    def get(self, key: str, timestamp: int) -> str:
        """
        Get the current value of a key at the given timestamp.
        
        Args:
            key: The key to retrieve
            timestamp: The current time
            
        Returns:
            The value if key exists and hasn't expired, None otherwise
        """
        records = self.data.get(key)

        if not records:
            return None

        end = len(records) - 1

        while end >= 0:
            record = records[end]

            if not self.ttl_valid(record, timestamp):
                end -= 1
                continue
            
            if record["timestamp"] <= timestamp:
                if not record["deleted"]:
                    return record["value"]
                else:
                    return None
            end -= 1
        
        return None
    
    def ttl_valid(self,record: object, query_ts: int) -> bool:
        """
        Designed to communicate if a record is valid
        """
        # Bad record
        ts = record.get("timestamp")
        ttl = record.get("ttl")        

        if not ttl:
            return True
        
        if not ts:
            return False
        
        if query_ts - ts < ttl:
            return True
        
        return False
        
    
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
        return self.get(key, timestamp)
    
    def delete(self, key: str, timestamp: int) -> None:
        """
        Delete a key at the given timestamp.
        
        Args:
            key: The key to delete
            timestamp: When this operation occurs
        """
        records = self.data[key]

        end = len(records) - 1
        while end >= 0:
            record = records[end]

            if record["timestamp"] <= timestamp:
                records.append({"timestamp": timestamp, "value": record["value"], "ttl": record["ttl"], "deleted": True})
            end -= 1    
        return None
