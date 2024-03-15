from db import Note 
from models import NoteIn, NoteOut

class NoteRepository:
    def __init__(self, session):
        self._session = session

    def get_note(self, id) -> NoteOut:
        note = self._session.get(Note, id)
        return NoteOut(name=note.name, description=note.description, done=note.done, id=note.id)

    def get_notes(self) -> list[NoteOut]:
        return [NoteOut(name=note.name, description=note.description, done=note.done, id=note.id) for note in self._session.query(Note).all()]

    def create_note(self, note: NoteIn):
        note = Note(name=note.name, description=note.descriotion, done=note.done, id=note.id)
        