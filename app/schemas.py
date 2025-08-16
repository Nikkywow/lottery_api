from pydantic import BaseModel, validator
from typing import List

class DrawCreate(BaseModel):
    pass

class DrawResponse(BaseModel):
    id: int
    status: str
    winning_numbers: List[int] = None

    class Config:
        orm_mode = True

class TicketCreate(BaseModel):
    numbers: List[int]
    draw_id: int

    @validator('numbers')
    def validate_numbers(cls, v):
        if len(v) != 5:
            raise ValueError("Ticket must contain exactly 5 numbers")
        if len(set(v)) != 5:
            raise ValueError("Numbers must be unique")
        if any(num < 1 or num > 36 for num in v):
            raise ValueError("Numbers must be between 1 and 36")
        return sorted(v)

class TicketResponse(BaseModel):
    id: int
    draw_id: int
    numbers: List[int]
    is_winner: bool

    class Config:
        orm_mode = True

class DrawResults(BaseModel):
    draw: DrawResponse
    tickets: List[TicketResponse]
    winning_numbers: List[int] = None