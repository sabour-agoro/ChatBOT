#configuration de la connexion a postgreSql 
import os 
from dotenv import load_dotenv
fom sqlmodel import creat_engine , Session 

load_dotenv()

sqlite_url = os.getenv("Database_url")

engine  = creat_engine(sqlite_url)

def get_Session():
    with Session(engine) as Session:
        yield session