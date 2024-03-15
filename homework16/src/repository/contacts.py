from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_, extract, and_

from src.database.models import Contact
from src.schemas import ContactIn, ContactUpdate

from datetime import date, datetime, timedelta

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def find_contact(keyword: str, skip: int, limit: int, db: Session) -> List[Contact]:
    word = f"%{keyword}%"
    query = db.query(Contact).filter(or_(Contact.name.ilike(word), Contact.lastname.ilike(word), Contact.email.ilike(word))).offset(skip).limit(limit).all()
    return query

async def create_contact(body: ContactIn, db: Session) -> Contact:
    contact = Contact(name=body.name, lastname=body.lastname, email=body.email, phone=body.phone, birthday=body.birthday, notes=body.notes)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        if body.name:
            contact.name = body.name
        if body.lastname:
            contact.lastname = body.lastname
        if body.email:
            contact.email = body.email
        if body.phone:
            contact.phone = body.phone
        if body.birthday:
            contact.birthday = body.birthday
        if body.notes:
            contact.notes = body.notes
        db.commit()
    return contact

# API powinno być w stanie pobrać listę kontaktów z datami urodzin na najbliższe 7 dni
async def get_contacts_birthday_for_next_seven_days(skip: int, limit: int, db: Session) -> List[Contact]:
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    query = db.query(Contact).filter(
        or_(
            and_(
            extract("month", today) == extract("month", next_week),
            extract("month", Contact.birthday) == extract("month", today),
            extract("day", Contact.birthday) >= extract("day", today),
            extract("day", Contact.birthday) <= extract("day", next_week)
            ),
            and_(
            extract("month", today) != extract("month", next_week),
            extract("month", Contact.birthday) == extract("month", today),
            extract("day", Contact.birthday) >= extract("day", today)
            ),
            and_(
                extract("month", today) != extract("month", next_week),
                extract("month", Contact.birthday) == extract("month", next_week),
                extract("day", Contact.birthday) <= extract("day", next_week)
            )
        )).order_by("birthday").offset(skip).limit(limit).all()
    return query