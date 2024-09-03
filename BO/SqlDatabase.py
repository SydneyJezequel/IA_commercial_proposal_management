from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BO.Quotation import Quotation, Base
import config
import re
import logging






class SqlDatabase:
    """ Classe de la BDD SQLite / Stocke les données des devis concurrents """



    def __init__(self, db_url=config.DB_URL):
        """ Constructeur / Initialisation de la base de données. """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


              
    """ Configuration des logs. """
    logging.basicConfig(level=logging.INFO)



    def save_quotation(self, quotations_data):
        """ Méthode qui enregistre un nouveau devis en BDD. """

        session = self.Session()

        try:
            # Nettoyage et conversion des valeurs numériques :
            quotations_data['montant_total'] = self.clean_and_convert_to_float(quotations_data.get('montant_total'))
            quotations_data['taux_tva'] = self.clean_and_convert_to_float(quotations_data.get('taux_tva'))
            quotations_data['total_ttc'] = self.clean_and_convert_to_float(quotations_data.get('total_ttc'))
            # Création de l'instance de Devis :
            quotation_instance = Quotation(**quotations_data)
            logging.info(f"DEVIS ENREGISTRÉ : {quotation_instance}")
            # Ajout du devis en BDD :
            session.add(quotation_instance)
            session.commit()
            # Préparation du résultat :
            result = {
                "id": quotation_instance.id,
                "devis": quotation_instance.devis,
                "entreprise": quotation_instance.entreprise,
                "adresse_entreprise": quotation_instance.adresse_entreprise,
                "date": quotation_instance.date,
                "client": quotation_instance.client,
                "adresse_client": quotation_instance.adresse_client,
                "code_postal_client": quotation_instance.code_postal_client,
                "description": quotation_instance.description,
                "montant_total": float(quotation_instance.montant_total),
                "taux_tva": float(quotation_instance.taux_tva),
                "total_ttc": float(quotation_instance.total_ttc),
                "conditions": quotation_instance.conditions,
                "debut_travaux": quotation_instance.debut_travaux,
            }
            logging.info(f"RÉSULTAT RENVOYÉ : {result}")
            return result

        except ValueError as ve:
            logging.error(f"Conversion des données échouée : {str(ve)}")
            session.rollback()
            return {"error": f"Conversion des données échouée : {str(ve)}"}

        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors de l'enregistrement du devis : {str(e)}")
            session.rollback()
            return {"error": f"Une erreur inattendue s'est produite lors de l'enregistrement du devis : {str(e)}"}
        
        finally:
            session.close()

    

    def clean_and_convert_to_float(self, value):
        """ Méthode qui nettoie et convertit une valeur en float. """

        try:
            if isinstance(value, str):
                # Suppression des caractères non numériques
                value = re.sub(r'[^\d.]', '', value)
            return float(value)

        except ValueError as ve:
            logging.error(f"Impossible de convertir la valeur en float : {value}")
            raise ValueError(f"Impossible de convertir la valeur en float : {value}") from ve
        except TypeError as te:
            logging.error(f"Type incorrect pour la conversion en float : {type(value).__name__}")
            raise TypeError(f"Type incorrect pour la conversion en float : {type(value).__name__}") from te



    def get_all_quotations(self):
        """ Méthode qui récupère tous les devis en BDD. """

        session = self.Session()
        quotations_list = []

        try:
            # Récupération des devis en BDD
            quotations_list = session.query(Quotation).all()

        except Exception as e:
            logging.info(f"Une erreur inattendue s'est produite lors de la récupération des devis : {e}")
            return {"error": f"Une erreur inattendue s'est produite lors de la récupération des devis : {str(e)}"}
        
        finally:
            session.close()

        return quotations_list

