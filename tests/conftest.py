import pytest
import asyncio

pytest_plugins = [
    'shared.infrastructure.pytest.fixtures',
    'shoes.infrastructure.pytest.fixtures',
]


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    res = policy.new_event_loop()
    asyncio.set_event_loop(res)
    res._close = res.close
    res.close = lambda: None

    yield res

    res._close()
