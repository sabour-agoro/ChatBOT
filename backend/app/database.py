#configuration de la connexion a postgreSql 
import os 
from dotenv import load_dotenv
from sqlmodel import create_engine , Session 

load_dotenv()

sqlite_url = os.getenv("Database_url")

engine  = create_engine(sqlite_url)

def get_session():
    with Session(engine) as Session:
        yield session