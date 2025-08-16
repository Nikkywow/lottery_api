from sqlalchemy import Column, Integer, String, Boolean, JSON
from .database import Base

class Draw(Base):
    __tablename__ = "draws"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="open")  # 'open' or 'closed'
    winning_numbers = Column(JSON, nullable=True)

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    draw_id = Column(Integer, index=True)
    numbers = Column(JSON)
    is_winner = Column(Boolean, default=False)