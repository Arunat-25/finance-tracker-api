import pytest

async def sum(a, b):
    return a + b

@pytest.mark.asyncio
async def test_api():
    assert await sum(1, 2) == 3