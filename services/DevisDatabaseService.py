from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BO.Devis import Devis, Base
import config






class DevisDatabaseService:
    """ Service pour gérer la base de données des devis """



    def __init__(self, db_url=config.DB_URL):
        """Initialisation de la base de données"""
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    

    def create_devis(self, devis_data):
        """ Méthode qui crée un nouveau devis et l'intègre en BDD """
        session = self.Session()
        devis_instance = Devis(**devis_data)

        try:
            session.add(devis_instance)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Erreur lors de la création du devis: {e}")
        finally:
            session.close()

        return {
            "id": devis_instance.id,
            "devis": devis_instance.devis,
            "entreprise": devis_instance.entreprise,
            "adresse_entreprise": devis_instance.adresse_entreprise,
            "date": devis_instance.date,
            "client": devis_instance.client,
            "adresse_client": devis_instance.adresse_client,
            "code_postal_client": devis_instance.code_postal_client,
            "description": devis_instance.description,
            "montant_total": float(devis_instance.montant_total),  # Conversion en float pour la sortie
            "taux_tva": float(devis_instance.taux_tva),  # Conversion en float pour la sortie
            "total_ttc": float(devis_instance.total_ttc),  # Conversion en float pour la sortie
            "conditions": devis_instance.conditions,
            "debut_travaux": devis_instance.debut_travaux,
        }



    def get_all_devis(self):
        """ Méthode qui récupère tous les devis en BDD """
        session = self.Session()
        devis_list = []
        
        try:
            devis_list = session.query(Devis).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des devis: {e}")
        finally:
            session.close()
        
        return devis_list

