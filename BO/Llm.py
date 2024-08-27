from openai import OpenAI
import config
from BO.VectorDatabase import VectorDataBase






class Llm:
    """ Classe du Modèle """



    def __init__(self):
        """ Constructeur """
        self.vector_database = VectorDataBase()



    def generate_answer(self, prompt):
        """ Méthode qui interroge le modèle """
        # Connexion à l'Api :
        client = OpenAI(
        base_url = config.MONSTER_API_URL,
        api_key = config.MONSTER_API_KEY
        )
        # Envoi de la requête au modèle :
        completion = client.chat.completions.create(
            model= "meta-llama/Meta-Llama-3-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Réduire pour une réponse plus déterministe
            top_p=0.8,        # Limiter les choix pour une réponse plus prévisible
            max_tokens=500,
            stream=True
        )
        # Traitement de la réponse :
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        return full_response



    def generate_commercial_proposal(self):
        """ Méthode qui utilise le modèle pour générer une offre commerciale """
        # Récupération des informations contextuelles
        context = "En vue de créer une offre commerciale et de nous positionner par rapport à nos concurrents, récupère les spécificités de notre entreprise et les devis des concurrents."
        data_context = self.vector_database.search_context(context)
        
        # Préparation du prompt en suivant le format Llama 3
        prompt = (
            "<|begin_of_text|>"
            "<|start_header_id|>system<|end_header_id|>"
            "You are an AI assistant specialized in generating commercial proposals based on company-specific information and competitor quotes.<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>"
            f"Génère moi une offre commerciale en prenant en compte les spécificités de notre entreprise et les devis des concurrents. Voici les détails : {data_context}<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>"
        )
        
        # Connexion à l'API
        client = OpenAI(
            base_url=config.MONSTER_API_URL,
            api_key=config.MONSTER_API_KEY
        )
        
        # Envoi de la requête au modèle
        completion = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Réduire pour une réponse plus déterministe
            top_p=0.8,        # Limiter les choix pour une réponse plus prévisible
            max_tokens=500,
            stream=True
        )
        
        # Traitement de la réponse
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        
        return full_response


    """
    def generate_commercial_proposal(self):
        # Méthode qui utilise le modèle pour générer une offre commerciale
        # Préparation du prompt :
        question = "Génère moi une offre commercial en prenant en compte les spécificités de notre entreprise et les devis des concurrents"
        context = "En vue de créer une offre commercial et de nous positionner par rapport à nos concurrents, récupère les spécificités de notre entreprise et les devis des concurrents"
        data_context = self.vector_database.search_context(context)
        prompt = {
            "question": question,
            "context": data_context
        }
        # Connexion à l'Api :
        client = OpenAI(
        base_url = config.MONSTER_API_URL,
        api_key = config.MONSTER_API_KEY
        )
        # Envoi de la requête au modèle :
        completion = client.chat.completions.create(
            model= config.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Réduire pour une réponse plus déterministe
            top_p=0.8,        # Limiter les choix pour une réponse plus prévisible
            max_tokens=500,
            stream=True
        )
        # Traitement de la réponse :
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        return full_response
    """
