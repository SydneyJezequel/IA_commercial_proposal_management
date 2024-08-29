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





    # ******************************* METHODE EN COURS DE MODIFICATION ******************************* #

    def generate_commercial_proposal(self):
        print("Exécution de generate_commercial_proposal() ")
        """ Méthode qui utilise le modèle pour générer une offre commerciale. """
        # ****** TEST ******** #
        print("********************** TEST ************************")
        db_vectorielle = VectorDataBase()
        documents = db_vectorielle.retrieve_all_documents()
        print(" TOUS LES DOCUMENTS DE LA BDD VECTORIELLE avec retrieve_all_documents() : ", documents)
        documents2 = db_vectorielle.search_context()
        print(" TOUS LES DOCUMENTS DE LA BDD VECTORIELLE avec db_vectorielle.search_context() : ", documents2)
        print("********************** TEST ************************")
        # ****** TEST ******** #
        # Récupération des informations contextuelles
        context = "En vue de créer un devis, récupère les spécificités de notre entreprise et les devis des concurrents."
        data_context = self.vector_database.search_context(context)
        print("CONTEXT ENVOYE : ", data_context)
        # Préparation du prompt en suivant le format Llama 3
        prompt = (
            "system\n"
            "You are an AI assistant specialized in generating highly competitive commercial proposals based on specific company information and competitor quotes. Ensure the proposal offers a lower total cost, more flexible payment conditions, and the earliest possible start date. Additionally, any cost reductions must be justified with strategic choices, such as the use of alternative materials, volume discounts, etc.\n"
            "user\n"
            f"Génère un devis qui surpasse les devis des concurrents en réduisant le coût total, en assouplissant les conditions de paiement, et en proposant la date de début des travaux la plus proche possible. Assure-toi que les réductions de coûts sont justifiées par des choix stratégiques. "
            "Les informations du devis doivent être renseignées dans le JSON suivant. Les informations déjà renseignées sont à conserver :\n"
            "{{\n"
            "    \"Numéro de devis\": \"" + config.NUMERO_DEVIS + "\",\n"
            "    \"Société\": \"" + config.SOCIETE + "\",\n"
            "    \"Adresse de la société\": \"" + config.ADRESSE_SOCIETE + "\",\n"
            "    \"Date du devis\": \"" + config.DATE_DEVIS + "\",\n"
            "    \"Nom du client\": \"\",\n"
            "    \"Adresse du client\": \"\",\n"
            "    \"Code Postal du client\": \"\",\n"
            "    \"Description du travail\": \"\",\n"
            "    \"Montant total HT\": \"\",\n"
            "    \"Taux de TVA\": \"\",\n"
            "    \"Montant total TTC\": \"\",\n"
            "    \"Début des travaux\": \"\",\n"
            "    \"Conditions de règlement\": \"\"\n"
            "}}\n"
            f"Détails : {data_context}\n"
            "assistant\n"
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
        # Traitement de la réponse avec validation des justifications
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
        print("FULL RESPONSE RECUPEREE : ", full_response)        
        # Validation et ajustement des justifications
        validated_response = self.validate_and_adjust_response(full_response)
        print("VALIDATED_REPONSE RECUPEREE : ", validated_response)
        return validated_response

    # ******************************* METHODE EN COURS DE MODIFICATION ******************************* #


    


    def validate_and_adjust_response(self, response):
        """ Méthode qui valide la réponse pour s'assurer que les réductions de coûts sont justifiées."""
        # Vérifie si le mot "justification" apparaît dans la réponse
        if "justification" not in response.lower():
            response += "\n(Note: Please ensure that all cost reductions are justified with strategic choices such as alternative materials, volume discounts, or other viable strategies.)"
        return response




















    """
    def generate_commercial_proposal(self):
        # Méthode qui utilise le modèle pour générer une offre commerciale
        # Récupération des informations contextuelles
        context = "En vue de créer une offre commerciale et de nous positionner par rapport à nos concurrents, récupère les spécificités de notre entreprise et les devis des concurrents."
        data_context = self.vector_database.search_context(context)
        
        # Préparation du prompt en suivant le format Llama 3 :
        prompt = (
            "<|begin_of_text|>"
            "<|start_header_id|>system<|end_header_id|>"
            "You are an AI assistant specialized in generating highly competitive commercial proposals based on specific company information and competitor quotes. Ensure the proposal offers a lower total cost, more flexible payment conditions, and the earliest possible start date. Additionally, any cost reductions must be justified with strategic choices, such as the use of alternative materials, volume discounts, etc.<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>"
            f"Génère une offre commerciale qui surpasse les devis des concurrents en réduisant le coût total, en assouplissant les conditions de paiement, et en proposant la date de début des travaux la plus proche possible. Assure-toi que les réductions de coûts sont justifiées par des choix stratégiques. Détails : {data_context}<|eot_id|>"
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





























    # ==> VERSION 2 :
    """
    def generate_commercial_proposal(self):
        # Méthode qui utilise le modèle pour générer une offre commerciale
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











    # ==> VERSION 1 :
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




