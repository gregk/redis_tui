"""
Redis client wrapper for the TUI application.

This module provides a wrapper around the Redis client with
async support and error handling.
"""

from typing import Any, Dict, List, Optional, Tuple
import redis.asyncio as redis
import json
import logging

logger = logging.getLogger(__name__)

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
        """Get Redis keys matching pattern."""
        return await self.client.keys(pattern)
        
    async def get_type(self, key: str) -> str:
        """Get type of Redis key."""
        return await self.client.type(key)
        
    async def get_value(self, key: str) -> Any:
        """Get value for Redis key."""
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

    async def get_key(self, key: str) -> Optional[str]:
        """Get value for a key."""
        try:
            key_type = await self.client.type(key)
            logger.debug(f"Key type for {key}: {key_type}")
            
            if key_type == "string":
                data = await self.client.get(key)
                logger.debug(f"String data for {key}: {data}")
                try:
                    parsed = json.loads(data)
                    return json.dumps(parsed, indent=2)
                except:
                    return data
            elif key_type == "hash":
                data = await self.client.hgetall(key)
                logger.debug(f"Hash data for {key}: {data}")
                return json.dumps(data, indent=2)
            elif key_type == "list":
                data = await self.client.lrange(key, 0, -1)
                logger.debug(f"List data for {key}: {data}")
                return json.dumps(data, indent=2)
            elif key_type == "set":
                data = await self.client.smembers(key)
                logger.debug(f"Set data for {key}: {data}")
                return json.dumps(list(data), indent=2)
            elif key_type == "zset":
                data = await self.client.zrange(key, 0, -1, withscores=True)
                logger.debug(f"ZSet data for {key}: {data}")
                return json.dumps(dict(data), indent=2)
            
            return None
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}", exc_info=True)
            return None
        
    async def get_key_type(self, key: str) -> str:
        """Get the type of a key."""
        return await self.client.type(key)
        
    async def get_all_keys(self) -> Dict[str, List[str]]:
        """Get all keys organized by namespace."""
        keys = {}
        redis_keys = await self.client.keys("*")
        for key in redis_keys:
            key_str = key if isinstance(key, str) else key.decode('utf-8')
            namespace = key_str.split(':', 1)[0] if ':' in key_str else 'other'
            if namespace not in keys:
                keys[namespace] = []
            keys[namespace].append(key_str)
        return keys 