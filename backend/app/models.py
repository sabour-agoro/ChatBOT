import os 
from sqlmodel import SQLModel , Field
from typing import Optional
from datetime import datetime


class User(SQLModel , table = True):
    __tablename__ = "users"
    id_user : Optional[int] = Field(default=None, primary_key =True)
    email : str = Field(unique=True)
    mot_de_passe : str
    nom_user : str 
    
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    id_conv : Optional[int] = Field(default=None, primary_key=True)
    title : str = Field(default="NOUVELLE DISCUSSION")
    date_creation : datetime = Field(default_factory=datetime.utcnow)
    id_user : int = Field(foreign_key="users.id_user")
    
class  Message (SQLModel, table=True):
    __tablename__="messages"
    id_ms : Optional[int] = Field(default = None, primary_key=True)
    id_conv:int = Field(foreign_key="conversations.id_conv")
    role:str
    contenu:str
    date_envoi:datetime= Field(default_factory=datetime.utcnow)
    
    