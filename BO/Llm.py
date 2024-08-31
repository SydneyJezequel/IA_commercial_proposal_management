from decimal import Decimal
from openai import OpenAI
import config
from BO.VectorDatabase import VectorDataBase
from BO.SqlDatabase import SqlDatabase






class Llm:
    """ Classe du Modèle """



    def __init__(self):
        """ Constructeur """



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
        print("Exécution de generate_commercial_proposal() ")
        """ Méthode qui utilise le modèle pour générer une offre commerciale. """

        # Récupération de nos informations commerciales :
        context = "En vue de créer un devis, récupère les éléments suivants relatifs à notre entreprise : les économies réalisées grâce à nous, nos avantages compétitifs, l’historique de nos projets , nos avantages tarifaire, nos références clients."
        self.vector_database = VectorDataBase()
        data_context = self.vector_database.search_context(context)
        print("ATOUTS DE NOTRE ENTREPRISE : ", data_context)

        # Récupération de la liste des devis concurrents : 
        sql_service = SqlDatabase()
        devis_list =  sql_service.get_all_devis()
        print("LISTE DES DEVIS CONCURRENTS : ", devis_list)

        # Filtrage des devis pour exclure ceux avec un montant total de 0.00
        valid_devis_list = [devis for devis in devis_list if devis.montant_total > 0.00 and devis.entreprise != "Non spécifié"]
        
        # Vérification si nous avons des devis valides
        if not valid_devis_list:
            raise ValueError("Aucun devis valide trouvé.")
    
        # Détermination du devis le plus bas
        lowest_quote = min(devis.montant_total for devis in valid_devis_list)
        print("DEVIS LE PLUS BAS : ", lowest_quote)

        # Convertir 0.95 en Decimal
        reduction = Decimal(config.RABAIS_APPLIQUE)

        # Appliquer la réduction
        reduced_quote = lowest_quote * reduction
        print("DEVIS APRES REDUCTION : ", reduced_quote)

        # Préparation du prompt en suivant le format Llama 3
           # Préparation du prompt en suivant le format Llama 3
        prompt = (
            "system\n"
            "Vous êtes un assistant IA spécialisé dans la génération d'offres commerciales très compétitives basées sur des informations spécifiques à l'entreprise et des devis concurrents. Assurez-vous que l'offre propose un coût total inférieur, des conditions de paiement plus flexibles et la date de début des travaux la plus rapide possible. De plus, toute réduction de coût doit être justifiée par des choix stratégiques, tels que l'utilisation de matériaux alternatifs, des remises sur les volumes, etc.\n"
            "user\n"
            f"Génère un devis qui est 5% moins cher que le devis le plus bas des concurrents. Le montant total doit être égal à {reduced_quote} et justifié par des choix stratégiques tels que l'utilisation de matériaux alternatifs ou des réductions sur les volumes."
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
            f"Détails au sujet de notre société : {data_context}\n"
            f"Liste des devis concurrents : {valid_devis_list}\n"
            "assistant\n"
        )
        # Connexion à l'API
        client = OpenAI(
            base_url=config.MONSTER_API_URL,
            api_key=config.MONSTER_API_KEY
        )
        # Envoi de la requête au modèle
        try:
            completion = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Réduire pour une réponse plus déterministe
                top_p=0.8,        # Limiter les choix pour une réponse plus prévisible
                max_tokens=500,
                stream=True
            )
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'appel à l'API : {e}")
            return {"error": str(e)}    
        # Traitement de la réponse avec validation des justifications
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
        print("REPONSE RENVOYEE PAR LE LLM : ", full_response)        
        # Validation et ajustement des justifications
        validated_response = self.validate_and_adjust_response(full_response)
        print("DEVIS FINAL RENVOYE : ", validated_response)
        return validated_response



    def validate_and_adjust_response(self, response):
        """ Méthode qui valide la réponse pour s'assurer que les réductions de coûts sont justifiées."""
        # Vérifie si le mot "justification" apparaît dans la réponse
        if "justification" not in response.lower():
            response += "\n(Note: Please ensure that all cost reductions are justified with strategic choices such as alternative materials, volume discounts, or other viable strategies.)"
        return response

