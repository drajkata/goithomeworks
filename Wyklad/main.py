from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from starlette import status
from sqlalchemy import text
from sqlalchemy.orm import Session
from db import get_db, Note
import time
from pathlib import Path

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
#  wszystko co będzie /static będzie dostępne
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": file_path}

# @app.get("/api/healthchecker")
# def root():
#     return {"message": "Welcome to FastAPI!!!"}

# @app.get("/api/healthchecker")
# def healthchecker(db: Session = Depends(get_db)):
#     try:
# # Make request
#         # result = db.execute("SELECT 1").fetchone()
#         result = db.execute(text("SELECT 1")).fetchone()
#         if result is None:
#             raise HTTPException(status_code=500, detail="Database is not configured correctly")
#         return {"message": "Welcome to FastAPI!"}
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Error connecting to the database")

# # http://localhost:8000/api/healthchecker



# # @app.get("/notes/new")
# # async def read_new_notes():
# #     return {"message": "Return new notes"}

# @app.get("/notes/{note_id}")
# async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10)):
#     return {"note": note_id}

# @app.get("/notes")
# async def read_notes(skip: int = 0, limit: int = 10):
#     return {"message": f"Return all notes: skip: {skip}, limit: {limit}"}


# @app.get("/notes")
# async def read_notes(skip: int = 0, limit: int = 10, q: str | None = None):
#     return {"message": f"Return all notes: skip: {skip}, limit: {limit}"}


# @app.get("/notes")
# async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10)):
#     return {"message": f"Return all notes: skip: {skip}, limit: {limit}"}


# class Note(BaseModel):
#     name: str
#     description: str
#     done: bool

# @app.post("/notes")
# async def create_note(note: Note):
#     return {"name": note.name, "description": note.description, "status": note.done}


class ResponseNoteModel(BaseModel):
    id: int = Field(default=1, ge=1)
    name: str
    description: str
    done: bool


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Здійснюємо запит
        result = db.execute("SELECT 1").fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.get("/notes")
async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)) -> \
        list[ResponseNoteModel]:
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes

@app.get("/notes/{note_id}", response_model=ResponseNoteModel)
async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10),
                    db: Session = Depends(get_db)) -> NoteOut:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note




@app.post("/notes", status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn, db: Session = Depends(get_db)):
    new_note = Note(name=note.name, description=note.description, done=note.done)
    session.add(new_note)
    session.comit()
    session.refresh(new_note)
    return new_note


# data = {"name": "Test note", "description": "Testing", "done": False}
# headers = {'Content-type': 'application/json'}

# response = requests.post('http://127.0.0.1:8000/notes', data=json.dumps(data), headers=headers)

# print(response.json())

@app.exception_handler(ValidationError)
def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Invalid input data"}
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
def unexpected_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred"},
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": file_path}