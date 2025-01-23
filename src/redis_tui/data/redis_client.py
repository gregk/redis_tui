"""
Redis client wrapper for the TUI application.

This module provides a wrapper around the Redis client with
async support and error handling.
"""

from typing import Any, Dict, List, Optional, Tuple
import redis.asyncio as redis

class RedisClient:
    """Wrapper for Redis client operations."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None
    ) -> None:
        """Initialize Redis client.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Optional Redis password
        """
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        
    async def get_keys(self, pattern: str = "*") -> List[str]:
        """Get Redis keys matching pattern.
        
        Args:
            pattern: Key pattern to match
            
        Returns:
            List of matching keys
        """
        return await self.client.keys(pattern)
        
    async def get_type(self, key: str) -> str:
        """Get type of Redis key.
        
        Args:
            key: Redis key
            
        Returns:
            Redis data type
        """
        return await self.client.type(key)
        
    async def get_value(self, key: str) -> Any:
        """Get value for Redis key.
        
        Args:
            key: Redis key
            
        Returns:
            Value of the key based on its type
        """
        key_type = await self.get_type(key)
        
        if key_type == "string":
            return await self.client.get(key)
        elif key_type == "hash":
            return await self.client.hgetall(key)
        elif key_type == "list":
            return await self.client.lrange(key, 0, -1)
        elif key_type == "set":
            return await self.client.smembers(key)
        elif key_type == "zset":
            return await self.client.zrange(key, 0, -1, withscores=True)
        
        return None
        
    async def get_ttl(self, key: str) -> int:
        """Get TTL for Redis key.
        
        Args:
            key: Redis key
            
        Returns:
            TTL in seconds, -1 if no TTL, -2 if key doesn't exist
        """
        return await self.client.ttl(key)
        
    async def delete_key(self, key: str) -> bool:
        """Delete Redis key.
        
        Args:
            key: Redis key
            
        Returns:
            True if key was deleted
        """
        return await self.client.delete(key) > 0
        
    async def set_ttl(self, key: str, ttl: int) -> bool:
        """Set TTL for Redis key.
        
        Args:
            key: Redis key
            ttl: TTL in seconds
            
        Returns:
            True if TTL was set
        """
        return await self.client.expire(key, ttl)
        
    async def close(self) -> None:
        """Close Redis connection."""
        await self.client.close() 