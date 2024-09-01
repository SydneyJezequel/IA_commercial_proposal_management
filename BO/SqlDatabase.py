from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BO.Devis import Devis, Base
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



    def save_devis(self, devis_data):
        """ Méthode qui enregistre un nouveau devis en BDD. """

        session = self.Session()

        try:
            # Nettoyage et conversion des valeurs numériques :
            devis_data['montant_total'] = self.clean_and_convert_to_float(devis_data.get('montant_total'))
            devis_data['taux_tva'] = self.clean_and_convert_to_float(devis_data.get('taux_tva'))
            devis_data['total_ttc'] = self.clean_and_convert_to_float(devis_data.get('total_ttc'))
            # Création de l'instance de Devis :
            devis_instance = Devis(**devis_data)
            logging.info(f"DEVIS ENREGISTRÉ (devis_instance) : {devis_instance}")
            # Ajout du devis en BDD :
            session.add(devis_instance)
            session.commit()
            # Préparation du résultat :
            result = {
                "id": devis_instance.id,
                "devis": devis_instance.devis,
                "entreprise": devis_instance.entreprise,
                "adresse_entreprise": devis_instance.adresse_entreprise,
                "date": devis_instance.date,
                "client": devis_instance.client,
                "adresse_client": devis_instance.adresse_client,
                "code_postal_client": devis_instance.code_postal_client,
                "description": devis_instance.description,
                "montant_total": float(devis_instance.montant_total),
                "taux_tva": float(devis_instance.taux_tva),
                "total_ttc": float(devis_instance.total_ttc),
                "conditions": devis_instance.conditions,
                "debut_travaux": devis_instance.debut_travaux,
            }
            logging.info(f"RÉSULTAT RENVOYÉ : {result}")
            return result

        except ValueError as ve:
            session.rollback()
            return {"error": f"Conversion des données échouée : {str(ve)}"}
        except Exception as e:
            session.rollback()
            return {"error": f"Une erreur s'est produite lors de l'enregistrement du devis : {str(e)}"}
        
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
            raise ValueError(f"Impossible de convertir la valeur en float : {value}")
        except TypeError as te:
            raise TypeError(f"Type incorrect pour la conversion en float : {type(value).__name__}")



    def get_all_devis(self):
        """ Méthode qui récupère tous les devis en BDD. """

        session = self.Session()
        devis_list = []

        try:
            # Récupération des devis en BDD
            devis_list = session.query(Devis).all()

        except Exception as e:
            logging.info(f"Erreur lors de la récupération des devis : {e}")
            return {"error": f"Une erreur s'est produite lors de la récupération des devis : {str(e)}"}
        
        finally:
            session.close()

        return devis_list

