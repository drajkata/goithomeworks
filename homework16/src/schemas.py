from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from typing import Optional

class ContactIn(BaseModel):
    name: str = Field(max_length=25)
    lastname: str = Field(max_length=50)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=15)
    birthday: date = Field()
    notes: str = Field(max_length=500)

    @validator('birthday', pre=True)
    def check_date_format(cls, v):
        if isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError("Invalid date format. Required format: YYYY-MM-DD")
        return v

class ContactOut(ContactIn):
    id: int
        
    class Config:
        orm_mode = True

class ContactUpdate(BaseModel):
    name: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    birthday: Optional[date]
    notes: Optional[str]

    @validator('birthday', pre=True)
    def check_date_format(cls, v):
        if isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError("Invalid date format. Required format: YYYY-MM-DD")
        return v

class ContactDelete(ContactIn):
    id: int
        
    class Config:
        orm_mode = True