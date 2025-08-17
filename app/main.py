from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/draws", response_model=schemas.DrawResponse)
def create_draw(db: Session = Depends(get_db)):

    open_draw = db.query(models.Draw).filter(models.Draw.status == "open").first()
    if open_draw:
        raise HTTPException(status_code=400, detail="There is already an open draw")

    db_draw = models.Draw()
    db.add(db_draw)
    db.commit()
    db.refresh(db_draw)
    return db_draw


@app.post("/tickets", response_model=schemas.TicketResponse)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):

    draw = db.query(models.Draw).filter(models.Draw.id == ticket.draw_id).first()
    if not draw:
        raise HTTPException(status_code=404, detail="Draw not found")
    if draw.status != "open":
        raise HTTPException(status_code=400, detail="Draw is not open")

    db_ticket = models.Ticket(
        draw_id=ticket.draw_id,
        numbers=ticket.numbers
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@app.post("/draws/{draw_id}/close", response_model=schemas.DrawResponse)
def close_draw(draw_id: int, db: Session = Depends(get_db)):
    draw = db.query(models.Draw).filter(models.Draw.id == draw_id).first()
    if not draw:
        raise HTTPException(status_code=404, detail="Draw not found")
    if draw.status == "closed":
        raise HTTPException(status_code=400, detail="Draw is already closed")


    winning_numbers = sorted(random.sample(range(1, 37), 5))
    draw.winning_numbers = winning_numbers
    draw.status = "closed"

    tickets = db.query(models.Ticket).filter(models.Ticket.draw_id == draw_id).all()
    for ticket in tickets:
        ticket.is_winner = sorted(ticket.numbers) == winning_numbers

    db.commit()
    db.refresh(draw)
    return draw


@app.get("/draws/{draw_id}/results", response_model=schemas.DrawResults)
def get_results(draw_id: int, db: Session = Depends(get_db)):
    draw = db.query(models.Draw).filter(models.Draw.id == draw_id).first()
    if not draw:
        raise HTTPException(status_code=404, detail="Draw not found")

    tickets = db.query(models.Ticket).filter(models.Ticket.draw_id == draw_id).all()

    return {
        "draw": draw,
        "tickets": tickets,
        "winning_numbers": draw.winning_numbers if draw.status == "closed" else None
    }
