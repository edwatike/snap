from sqlalchemy import Column, String, Integer
from app.db import Base, SessionLocal

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    email = Column(String)

def save_result(url: str, emails: list):
    db = SessionLocal()
    for email in emails:
        result = Result(url=url, email=email)
        db.add(result)
    db.commit()
    db.close() 