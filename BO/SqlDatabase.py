from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BO.Devis import Devis, Base
import config
import re






class SqlDatabase:
    """ Service pour gérer la base de données des devis """



    def __init__(self, db_url=config.DB_URL):
        """Initialisation de la base de données"""
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.clear_database()  # Supprime tout le contenu de la BDD à chaque instanciation
        Base.metadata.create_all(self.engine)
        """

    def clear_database(self):
        """ Méthode qui supprime tout le contenu de la BDD """
        print(" ********************* SUPPRESSION DE TOUTES LES DONNÉES DE LA BDD ********************* ")
        # Supprime toutes les tables
        Base.metadata.drop_all(self.engine)
        print(" ********************* BASE DE DONNÉES VIDÉE ********************* ")

              

    def save_devis(self, devis_data):
        """ Méthode qui crée un nouveau devis et l'intègre en BDD """
        print(" ********************* ENREGISTREMENT D'UN DEVIS ********************* ")
        session = self.Session()
        devis_data['montant_total'] = self.clean_and_convert_to_float(devis_data.get('montant_total'))
        devis_data['taux_tva'] = self.clean_and_convert_to_float(devis_data.get('taux_tva'))
        devis_data['total_ttc'] = self.clean_and_convert_to_float(devis_data.get('total_ttc'))
        print("DONNEES DES DEVIS: ", devis_data)
        devis_instance = Devis(**devis_data)
        print("DEVIS ENREGISTRE (devis_instance): ", devis_instance)
        try:
            session.add(devis_instance)
            session.commit()
            
            # Accéder aux attributs ici avant de fermer la session
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
        print(" ********************* FIN ENREGISTREMENT ********************* ")
        return result

    

    def clean_and_convert_to_float(self, value):
        """ Méthode qui nettoie la valeur en retirant les caractères non numériques et la convertit en float. """
        if isinstance(value, str):
            # Suppression des caractères non numériques :
            value = re.sub(r'[^\d.]', '', value)
            # Conversion en float :
            return float(value)
        return float(value)  # Si c'est déjà un float ou un int



    def get_all_devis(self):
        """ Méthode qui récupère tous les devis en BDD. """
        session = self.Session()
        devis_list = []
        try:
            devis_list = session.query(Devis).all()
        except Exception as e:
            print(f"Erreur lors de la récupération des devis: {e}")
        finally:
            session.close()
        return devis_list

