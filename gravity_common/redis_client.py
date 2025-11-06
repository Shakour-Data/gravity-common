"""
Redis utilities for caching and pub/sub.

Independent Redis helpers that any microservice can use.
"""

from typing import Any, Optional, Union
import json
from datetime import timedelta
import redis.asyncio as aioredis
from redis.asyncio import Redis


class RedisClient:
    """
    Async Redis client wrapper.
    
    Each microservice can create its own instance for caching and pub/sub.
    """
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        max_connections: int = 50,
        decode_responses: bool = True,
    ):
        """
        Initialize Redis client.
        
        Args:
            redis_url: Redis connection URL
            max_connections: Maximum number of connections
            decode_responses: Whether to decode responses to strings
        """
        self.redis_url = redis_url
        self.max_connections = max_connections
        self.decode_responses = decode_responses
        self._client: Optional[Redis] = None
    
    async def connect(self) -> None:
        """Establish Redis connection."""
        if not self._client:
            self._client = await aioredis.from_url(
                self.redis_url,
                max_connections=self.max_connections,
                decode_responses=self.decode_responses,
            )
    
    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None
    
    async def get(self, key: str) -> Optional[str]:
        """
        Get value by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self._client:
            await self.connect()
        return await self._client.get(key)
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[Union[int, timedelta]] = None,
    ) -> bool:
        """
        Set value with optional expiration.
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds or timedelta
            
        Returns:
            True if successful
        """
        if not self._client:
            await self.connect()
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        return await self._client.set(key, value, ex=expire)
    
    async def delete(self, *keys: str) -> int:
        """
        Delete one or more keys.
        
        Args:
            keys: Keys to delete
            
        Returns:
            Number of keys deleted
        """
        if not self._client:
            await self.connect()
        return await self._client.delete(*keys)
    
    async def exists(self, key: str) -> bool:
        """
        Check if key exists.
        
        Args:
            key: Key to check
            
        Returns:
            True if exists, False otherwise
        """
        if not self._client:
            await self.connect()
        return await self._client.exists(key) > 0
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """
        Increment key value.
        
        Args:
            key: Key to increment
            amount: Amount to increment by
            
        Returns:
            New value after increment
        """
        if not self._client:
            await self.connect()
        return await self._client.incrby(key, amount)
    
    async def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration on a key.
        
        Args:
            key: Key to set expiration on
            seconds: Expiration time in seconds
            
        Returns:
            True if successful
        """
        if not self._client:
            await self.connect()
        return await self._client.expire(key, seconds)
    
    async def get_json(self, key: str) -> Optional[dict]:
        """
        Get JSON value and parse it.
        
        Args:
            key: Cache key
            
        Returns:
            Parsed JSON or None
        """
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None
    
    async def set_json(
        self,
        key: str,
        value: dict,
        expire: Optional[Union[int, timedelta]] = None,
    ) -> bool:
        """
        Set JSON value.
        
        Args:
            key: Cache key
            value: Dictionary to cache
            expire: Expiration time
            
        Returns:
            True if successful
        """
        return await self.set(key, json.dumps(value), expire)
    
    async def health_check(self) -> bool:
        """
        Check if Redis connection is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            if not self._client:
                await self.connect()
            await self._client.ping()
            return True
        except Exception:
            return False
