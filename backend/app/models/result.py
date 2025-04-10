from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime
from ..db import Base, engine

class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

async def save_result(url: str, title: str, session: AsyncSession) -> Result:
    db_result = Result(url=url, title=title)
    session.add(db_result)
    await session.commit()
    await session.refresh(db_result)
    return db_result 