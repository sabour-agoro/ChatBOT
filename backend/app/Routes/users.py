from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import session
from jose import jwt, JWTError
from app import models, schema, auth
from app.database import get_db

router = APIRouter(
    prefix = "/users", 
    tags = ["users"]
      ) 

@router.post("/register",reponse_model=schema.UserResponse)
def register(user: schema.UserCreate, db: session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
          raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    
    # Créer le nouvel utilisateur
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schema.Token)
def login(user: schema.UserLogin, db: session = Depends(get_db)):
    
   # Connexion utilisateur - renvoie un token JWT
    
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )
    
    access_token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schema.UserResponse)
def get_current_user(token: str, db: session = Depends(get_db)):
    
   # Récupérer les informations de l'utilisateur connecté
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")
    
    
return {"message": "Inscription réussie"} 
