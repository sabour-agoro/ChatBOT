from fastapi import APIRouter, Depends
from sqlmodel import Session, select 
from ..database import get_session
from ..models import Message
from ..services.mistral_ai import mistral_service
from ..models import Conversation

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/ask")
async def ask_mistral(prompt: str):
    response = await mistral_service.generate_response(prompt)
    return {"status": "success", "answer": response}

# #savegarde des messages dans supabase
@router.post("/ask/{id_conv}")
async def chat_endpoint(id_conv: int, prompt: str, session: Session = Depends(get_session)):
    # on recuperer l'historique pour sauvegarder dans supabase 
    statement = select(Message).where(Message.id_conv == id_conv).order_by(Message.date_envoi)
    historique = session.exec(statement).all()
    
    #  Enregistrer le message de l'utilisateur
    user_msg = Message(id_conv=id_conv, role="user", contenu=prompt)
    session.add(user_msg)
    
    reponse_ia = await mistral_service.generate_response(prompt)
    
    
    ai_msg = Message(id_conv=id_conv, role="assistant", contenu=reponse_ia)
    session.add(ai_msg)
    session.commit()
    
    return {"reponse": reponse_ia}


@router.post("/new")
async def create_conversation(id_user: int, title: str = "Nouvelle discussion", session: Session = Depends(get_session)):
    new_conv = Conversation(id_user=id_user, title=title)
    session.add(new_conv)
    session.commit()
    session.refresh(new_conv) 
    return {"id_conv": new_conv.id_conv, "message": "Discussion créée !"}