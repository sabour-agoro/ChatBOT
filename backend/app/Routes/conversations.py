from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Conversation, Message
from typing import List

router = APIRouter(prefix="/conversations", tags=["Conversations"])

#creer les conv
@router.post("/create")
async def create_conv(id_user: int, title: str = "Nouvelle discussion", session: Session = Depends(get_session)):
    new_conv = Conversation(id_user=id_user, title=title)
    session.add(new_conv)
    session.commit()
    session.refresh(new_conv)
    return {"status": "success", "id_conv": new_conv.id_conv, "title": new_conv.title}

# lister les conv
@router.get("/user/{id_user}", response_model=List[Conversation])
async def get_user_conversations(id_user: int, session: Session = Depends(get_session)):
    statement = select(Conversation).where(Conversation.id_user == id_user)
    results = session.exec(statement).all()
    return results

# supprimer conv methode cascade 
@router.delete("/{id_conv}")
async def delete_conversation(id_conv: int, session: Session = Depends(get_session)):
    conv = session.get(Conversation, id_conv)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")
    session.delete(conv)
    session.commit()
    return {"message": "Discussion supprimée avec succès"}