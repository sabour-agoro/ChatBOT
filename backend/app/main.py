#point d'entree de l'application 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_route():
    return {"le serveur est connecté a la base de donnees supabase "}