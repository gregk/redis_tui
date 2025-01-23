"""
Tests for Redis client operations.
"""

import pytest
from redis_tui.data.redis_client import RedisClient
from redis_tui.data.sample_data import SAMPLE_DATA, load_sample_data

@pytest.fixture
async def redis_client():
    """Create a Redis client for testing."""
    client = RedisClient(db=15)  # Use separate DB for testing
    yield client
    await client.client.flushdb()  # Clean up after tests
    await client.close()

@pytest.mark.asyncio
async def test_load_sample_data(redis_client):
    """Test loading sample data."""
    await load_sample_data(redis_client)
    keys = await redis_client.get_keys()
    assert len(keys) == len(SAMPLE_DATA)

@pytest.mark.asyncio
async def test_get_string_value(redis_client):
    """Test retrieving string values."""
    await load_sample_data(redis_client)
    value = await redis_client.get_value("config:api:endpoint")
    assert value == SAMPLE_DATA["config:api:endpoint"]["value"]

@pytest.mark.asyncio
async def test_get_hash_value(redis_client):
    """Test retrieving hash values."""
    await load_sample_data(redis_client)
    value = await redis_client.get_value("user:1000")
    assert value == SAMPLE_DATA["user:1000"]["value"]

@pytest.mark.asyncio
async def test_get_list_value(redis_client):
    """Test retrieving list values."""
    await load_sample_data(redis_client)
    value = await redis_client.get_value("cart:user:1000:items")
    assert value == SAMPLE_DATA["cart:user:1000:items"]["value"]

@pytest.mark.asyncio
async def test_get_set_value(redis_client):
    """Test retrieving set values."""
    await load_sample_data(redis_client)
    value = await redis_client.get_value("categories:electronics")
    assert set(value) == set(SAMPLE_DATA["categories:electronics"]["value"])

@pytest.mark.asyncio
async def test_get_zset_value(redis_client):
    """Test retrieving sorted set values."""
    await load_sample_data(redis_client)
    value = await redis_client.get_value("ratings:product:1")
    expected = [(member, score) for member, score in SAMPLE_DATA["ratings:product:1"]["value"]]
    assert value == expected

@pytest.mark.asyncio
async def test_get_ttl(redis_client):
    """Test retrieving TTL values."""
    await load_sample_data(redis_client)
    ttl = await redis_client.get_ttl("cache:user:1000:preferences")
    assert ttl <= SAMPLE_DATA["cache:user:1000:preferences"]["ttl"]

@pytest.mark.asyncio
async def test_delete_key(redis_client):
    """Test deleting keys."""
    await load_sample_data(redis_client)
    assert await redis_client.delete_key("user:1000")
    value = await redis_client.get_value("user:1000")
    assert value is None

@pytest.mark.asyncio
async def test_set_ttl(redis_client):
    """Test setting TTL on keys."""
    await load_sample_data(redis_client)
    assert await redis_client.set_ttl("user:1000", 3600)
    ttl = await redis_client.get_ttl("user:1000")
    assert 0 < ttl <= 3600 