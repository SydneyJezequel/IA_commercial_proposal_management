from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BO.Devis import Devis, Base
import config
import re






class SqlDatabase:
    """ Classe de la BDD SQLite / Stocke les données des devis concurrents """



    def __init__(self, db_url=config.DB_URL):
        """ Initialisation de la base de données """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

              

    def save_devis(self, devis_data):
        """ Méthode qui enregistre un nouveau devis en BDD """
        session = self.Session()
        devis_data['montant_total'] = self.clean_and_convert_to_float(devis_data.get('montant_total'))
        devis_data['taux_tva'] = self.clean_and_convert_to_float(devis_data.get('taux_tva'))
        devis_data['total_ttc'] = self.clean_and_convert_to_float(devis_data.get('total_ttc'))
        devis_instance = Devis(**devis_data)
        print("DEVIS ENREGISTRE (devis_instance): ", devis_instance)
        try:
            # Ajout du devis en BDD :
            session.add(devis_instance)
            session.commit()
            # Préparation renvoi devis sous forme de dictionnaire :
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
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de la création du devis: {e}")
            return None
        finally:
            session.close()
        print("RESULTAT RENVOYE : ", result)
        return result

    

    def clean_and_convert_to_float(self, value):
        """ Méthode qui corrige un nombre """
        if isinstance(value, str):
            # Suppression des caractères non numériques :
            value = re.sub(r'[^\d.]', '', value)
            # Conversion en float :
            return float(value)
        return float(value)



    def get_all_devis(self):
        """ Méthode qui récupère tous les devis en BDD """
        session = self.Session()
        devis_list = []
        try:
            # Récupération des devis en BDD :
            devis_list = session.query(Devis).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des devis: {e}")
        finally:
            session.close()
        return devis_list

