from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///school.db")
# engine = create_engine("postgresql+psycopg2://drajkata:drajkata@localhost:5432/school.db")
Session = sessionmaker(bind=engine)
session = Session()
