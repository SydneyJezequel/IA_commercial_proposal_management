from decimal import Decimal
from openai import OpenAI
import config
from BO.VectorDatabase import VectorDataBase
from BO.SqlDatabase import SqlDatabase
import logging






class Llm:
    """ Classe du Modèle """



    def __init__(self):
        """ Constructeur """



    """ Configuration des logs. """
    logging.basicConfig(level=logging.INFO)



    def generate_commercial_proposal(self):
        """ Méthode qui génère une offre commerciale via le LLM. """

        try:
            # Récupération de nos informations commerciales :
            data_context = self.get_company_info()
            # Récupération des devis concurrents : 
            valid_devis_list = self.get_competitor_quotes()
            # Détermination du devis le plus bas et application de la réduction :
            free_amount = self.calculate_reduced_quote(valid_devis_list)
            # Calcul du montant TTC :
            vat_rate = valid_devis_list[0].taux_tva / 100
            ttc_amount = self.calculate_ttc_amount(free_amount, vat_rate)
            logging.info(f"Montant ht : {free_amount}, tva : {vat_rate}, Montant ttc : {ttc_amount}")
            # Préparation du prompt :
            prompt = (
                "system\n"
                "Vous êtes un assistant IA spécialisé dans la génération d'offres commerciales très compétitives basées sur des informations spécifiques à l'entreprise et des devis concurrents. "
                "Assurez-vous que l'offre propose un coût total inférieur, des conditions de paiement plus flexibles. "
                "De plus, toute réduction de coût doit être justifiée par des choix stratégiques, tels que l'utilisation de matériaux alternatifs, des remises sur les volumes, des partenariats de long terme avec des fournisseurs pour obtenir des tarifs préférentiels, etc.\n"
                "user\n"
                f"Génère un devis qui est 5% moins cher que le devis le plus bas des concurrents. Le montant total HT doit être égal à {free_amount} et justifié par des choix stratégiques tels que l'utilisation de matériaux alternatifs ou des réductions sur les volumes. "
                f"Le montant total TTC doit correspondre à {ttc_amount}. "
                "Les informations du devis doivent être renseignées dans le JSON suivant. Les nom, adresse et code postal du client sont les mêmes que sur les devis des concurrents. La date de début de travaux doit être inférieure à celles des devis des concurrents. Les informations déjà renseignées sont à conserver :\n"
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
                "    \"Début des travaux\": \"" + config.DATE_DEBUT_TRAVAUX + "\",\n"
                "    \"Conditions de règlement\": \"\"\n"
                "}}\n"
                f"Détails au sujet de notre société : {data_context}\n"
                f"Liste des devis concurrents : {valid_devis_list}\n"
                "assistant\n"
            )
            # Appel de la méthode generate_answer pour interroger le LLM :
            full_response = self.generate_answer(prompt)
            # Validation de la réponse :
            validated_response = self.validate_and_adjust_response(full_response)
            logging.info(f"REPONSE RENVOYEE PAR LE LLM : {full_response}")        
            logging.info(f"Devis Final généré : {validated_response}")
            return validated_response

        except ValueError as ve:
            logging.error(f"Erreur de validation des données : {str(ve)}")
            return {"error": f"Erreur de validation des données : {str(ve)}"}
        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors de la génération de la proposition commerciale : {str(e)}")
            return {"error": f"Une erreur inattendue s'est produite lors de la génération de la proposition commerciale : {str(e)}"}



    def generate_answer(self, prompt):
        """ Méthode qui interroge le LLM. """

        try:
            # Config de l'Api :
            client = OpenAI(
                base_url=config.MONSTER_API_URL,
                api_key=config.MONSTER_API_KEY
            )
            # Exécution de la requête :
            completion = client.chat.completions.create(
                model=config.MODEL_NAME,
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

        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors de l'interrogation du LLM : {str(e)}")
            return {"error": f"Une erreur inattendue s'est produite lors de l'interrogation du LLM : {str(e)}"}



    def get_company_info(self):
        """ Méthode qui récupère les informations de l'entreprise. """

        try:
            context = (
                "En vue de créer un devis, récupère les éléments suivants relatifs à notre entreprise : "
                "les économies réalisées grâce à nous, nos avantages compétitifs, l’historique de nos projets, "
                "nos avantages tarifaires, nos références clients."
            )
            self.vector_database = VectorDataBase()
            data_context = self.vector_database.search_context(context)
            logging.info(f"Avantages compétitifs de l'entreprise : {data_context}")
            return data_context

        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors de la récupération des informations de l'entreprise : {str(e)}")
            raise RuntimeError(f"Une erreur inattendue s'est produite lors de la récupération des informations de l'entreprise : {str(e)}") from e



    def get_competitor_quotes(self):
        """ Méthode qui récupère les devis des concurrents. """

        try:
            # Récupération des devis :
            sql_service = SqlDatabase()
            devis_list = sql_service.get_all_quotations()
            logging.info(f"Liste des devis : {devis_list}")
            # Filtrage des devis pour exclure ceux avec un montant total de 0.00 :
            valid_devis_list = [
                devis for devis in devis_list 
                if devis.montant_total > 0.00 and devis.entreprise != "Non spécifié"
            ]
            if not valid_devis_list:
                raise ValueError("Aucun devis valide trouvé.")
            return valid_devis_list

        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors de la récupération des devis concurrents : {str(e)}")
            raise RuntimeError(f"Une erreur inattendue s'est produite lors de la récupération des devis concurrents : {str(e)}") from e



    def calculate_reduced_quote(self, valid_devis_list):
        """ Calcule le montant ht du devis après réduction. """

        try:
            # Détermination du devis le plus bas :
            lowest_quote = min(devis.montant_total for devis in valid_devis_list)
            # Conversion de la réduction en décimal :
            reduction = Decimal(config.RABAIS_APPLIQUE)
            # Appliquer la réduction :
            reduced_quote = lowest_quote * reduction
            logging.info(f"Devis le plus bas : {lowest_quote} Devis après réduction : {reduced_quote}")
            return reduced_quote

        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors du calcul du devis réduit : {str(e)}")
            raise RuntimeError(f"Une erreur inattendue s'est produite lors du calcul du devis réduit : {str(e)}") from e



    def calculate_ttc_amount(self, free_amount, vat_rate):
        """ Méthode qui calcule le montant total ttc du devis sur la base du montant ht """

        try:
            # Calcul du montant ttc du devis :
            ttc_amount = free_amount * (1 + vat_rate)
            return ttc_amount
        
        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors du calcul du montant ttc : {str(e)}")
            raise RuntimeError(f"Une erreur inattendue s'est produite lors du calcul du montant ttc : {str(e)}") from e



    def validate_and_adjust_response(self, response):
        """ Méthode qui valide la réponse pour s'assurer que les réductions de coûts sont justifiées. """

        try:
            if "justification" not in response.lower():
                response += "\n(Note: Veuillez vous assurer que toutes les réductions de coûts sont justifiées par des choix stratégiques tels que l'utilisation de matériaux alternatifs, des remises sur les volumes ou d'autres stratégies viables.)"
            return response

        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors de la validation de la réponse : {str(e)}")
            raise RuntimeError(f"Une erreur inattendue s'est produite lors de la validation de la réponse : {str(e)}") from e

