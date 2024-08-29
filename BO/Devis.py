from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker






# Déclaration de la BDD in memory
Base = declarative_base()






class Devis(Base):
    """Classe représentant un devis, mappée à une table SQL"""

    __tablename__ = 'devis'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    devis = Column(String(50), default='Non spécifié')
    entreprise = Column(String(255), default='Non spécifié')
    adresse_entreprise = Column(String(255), default='Non spécifié')
    date = Column(String(50), default='Non spécifié')
    client = Column(String(255), default='Non spécifié')
    adresse_client = Column(String(255), default='Non spécifié')
    code_postal_client = Column(String(20), default='Non spécifié')
    description = Column(String(1000), default='')
    montant_total = Column(Numeric(10, 2), default=0.00)
    taux_tva = Column(Numeric(5, 2), default=0.00)
    total_ttc = Column(Numeric(10, 2), default=0.00)
    conditions = Column(String(1000), default='Non spécifié')
    debut_travaux = Column(String(50), default='Non spécifié')

    def __repr__(self):
        return (f"Devis(Devis={self.devis}, Entreprise={self.entreprise}, "
                f"Adresse Entreprise={self.adresse_entreprise}, Date={self.date}, "
                f"Client={self.client}, Adresse Client={self.adresse_client}, "
                f"Code Postal Client={self.code_postal_client}, Description={self.description}, "
                f"Montant Total={self.montant_total}, Taux TVA={self.taux_tva}, "
                f"Total TTC={self.total_ttc}, Conditions={self.conditions}, "
                f"Début Travaux={self.debut_travaux})")

