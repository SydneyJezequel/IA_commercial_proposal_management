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
        """ Méthode qui interroge le Llm """
        # Config de l'Api :
        client = OpenAI(
        base_url = config.MONSTER_API_URL,
        api_key = config.MONSTER_API_KEY
        )
        # Exécution de la requête :
        completion = client.chat.completions.create(
            model= "meta-llama/Meta-Llama-3-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            top_p=0.8,
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
        """ Méthode génère une offre commerciale via le LLM. """
        # Récupération de nos informations commerciales :
        data_context = self.get_company_info()
        # Récupération des devis concurrents : 
        valid_devis_list = self.get_competitor_quotes()
        # Détermination du devis le plus bas et application de la réduction :
        reduced_quote = self.calculate_reduced_quote(valid_devis_list)
        # Préparation du prompt :
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
        # Config de l'Api :
        client = OpenAI(
            base_url=config.MONSTER_API_URL,
            api_key=config.MONSTER_API_KEY
        )
        # Exécution de la requête :
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
        # Traitement de la réponse :
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
        # Validation de la réponse :
        validated_response = self.validate_and_adjust_response(full_response)
        print("REPONSE RENVOYEE PAR LE LLM : ", full_response)        
        print("Devis Final généré : ", validated_response)
        return validated_response



    def get_company_info(self):
        """ Méthode qui récupère les informations de l'entreprise """
        context = (
            "En vue de créer un devis, récupère les éléments suivants relatifs à notre entreprise : "
            "les économies réalisées grâce à nous, nos avantages compétitifs, l’historique de nos projets, "
            "nos avantages tarifaires, nos références clients."
        )
        self.vector_database = VectorDataBase()
        data_context = self.vector_database.search_context(context)
        print("Avantages compétitifs de l'entreprise : ", data_context)
        return data_context



    def get_competitor_quotes(self):
        """ Méthode qui récupère les devis des concurrents """
        # Récupération des devis :
        sql_service = SqlDatabase()
        devis_list = sql_service.get_all_devis()
        print("Liste des devis : ", devis_list)
        # Filtrage des devis pour exclure ceux avec un montant total de 0.00 :
        valid_devis_list = [
            devis for devis in devis_list 
            if devis.montant_total > 0.00 and devis.entreprise != "Non spécifié"
        ]
        if not valid_devis_list:
            raise ValueError("Aucun devis valide trouvé.")
        return valid_devis_list



    def calculate_reduced_quote(self, valid_devis_list):
        """ Calcule le devis après réduction """
        # Détermination du devis le plus bas :
        lowest_quote = min(devis.montant_total for devis in valid_devis_list)
        # Conversion de la réduction en décimal :
        reduction = Decimal(config.RABAIS_APPLIQUE)
        # Appliquer la réduction :
        reduced_quote = lowest_quote * reduction
        print("devis le plus bas : ", lowest_quote, " devis après réduction : ", reduced_quote)
        return reduced_quote



    def validate_and_adjust_response(self, response):
        """ Méthode qui valide la réponse pour s'assurer que les réductions de coûts sont justifiées """
        if "justification" not in response.lower():
            response += "\n(Note: Veuillez vous assurer que toutes les réductions de coûts sont justifiées par des choix stratégiques tels que l'utilisation de matériaux alternatifs, des remises sur les volumes ou d'autres stratégies viables.)"
        return response

