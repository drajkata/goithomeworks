from sqlalchemy import create_engine, Integer, String, ForeignKey, select, Text, and_, desc, func, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship

# engine = create_engine("sqlite:///:memory:", echo=False)
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    group_id: Mapped[int] = mapped_column("group_id", Integer, ForeignKey("groups.id", onupdate="CASCADE", ondelete="CASCADE"))
    group: Mapped["Group"] = relationship(Group, passive_updates=True, passive_deletes=True)

class Lecturer(Base):
    __tablename__ = 'lecturers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    lecturer_id: Mapped[int] = mapped_column("lecturer_id", Integer, ForeignKey("lecturers.id", onupdate="CASCADE", ondelete="CASCADE"))
    lecturer: Mapped["Lecturer"] = relationship(Lecturer, passive_updates=True, passive_deletes=True)

class Assessment(Base):
    __tablename__ = 'assessments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    assessment: Mapped[str] = mapped_column(String)
    student_id: Mapped[int] = mapped_column("student_id", Integer, ForeignKey("students.id", onupdate="CASCADE", ondelete="CASCADE"))
    student: Mapped["Student"] = relationship(Student, passive_updates=True, passive_deletes=True)
    subject_id: Mapped[int] = mapped_column("subject_id", Integer, ForeignKey("subjects.id", onupdate="CASCADE", ondelete="CASCADE"))
    student: Mapped["Subject"] = relationship(Subject, passive_updates=True, passive_deletes=True)
    created_at: Mapped["Date"] = mapped_column(Date)


# Base.metadata.create_all(engine)








