#point d'entree de l'application 

from fastapi import FastAPI
from .routes import chat, users, conversations  

app = FastAPI(title = "Chatbot API")

app.include_router(chat.router)
app.include_router(users.router)
app.include_router(conversations.router)
@app.get("/")
def read_root():
    return {"status": "Online"}