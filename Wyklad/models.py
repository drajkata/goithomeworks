from pydantic import BaseModel, Field

class NoteIn(BaseModel):
    name: str
    description: str
    done: bool

class NoteOut(NoteIn):
    name: str
    description: str
    done: bool