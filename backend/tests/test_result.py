import pytest
from app.models.result import Result, save_result
from app.db import init_db, get_session
from sqlalchemy import select

@pytest.fixture(autouse=True)
async def setup_db():
    await init_db()
    yield
    async with get_session() as session:
        await session.execute(Result.__table__.delete())
        await session.commit()

@pytest.mark.asyncio
async def test_save_result():
    # Test data
    test_url = "https://example.com"
    test_title = "Example Title"
    
    # Save result
    async with get_session() as session:
        result = await save_result(test_url, test_title, session)
        
        # Verify result
        query = select(Result)
        db_result = await session.execute(query)
        results = db_result.scalars().all()
        
        assert len(results) == 1
        assert results[0].url == test_url
        assert results[0].title == test_title
        assert results[0].created_at is not None 