#logique pur d'appel de l'api mistral ai 
import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("Cle_mistral_ai")
client = Mistral(api_key = api_key)

class MistralAIService:
    async def generate_response(self, user_message : str):
        

        try :
        
            model = "mistral-small-latest"
            chat_response = client.chat.complete(model = model,
                                         messages = [
                                             {"role": "system", "content": "Tu es un assistant utile et poli et tu t'appelles freeze."},
                                             {"role": "user", "content": user_message},
                                         ])
    
            return chat_response.choices[0].message.content
        except Exception as e:
        
            print(f"Erreur lors de l'appel a Mistral : {e}")
            return "Désolé , j'ai un petit problème technique pour répondre."

    
mistral_service = MistralAIService()
