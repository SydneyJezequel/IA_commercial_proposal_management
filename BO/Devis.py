

class Devis:
    """ Classe représentant un devis """



    def __init__(self, devis='Non spécifié', entreprise='Non spécifié', adresse_entreprise='Non spécifié',
                 date='Non spécifié', client='Non spécifié', adresse_client='Non spécifié', code_postal_client='Non spécifié',
                 description='', montant_total='Non spécifié', taux_tva='Non spécifié', total_ttc='Non spécifié', 
                 conditions='Non spécifié', debut_travaux='Non spécifié'):
        """ Constructeur """
        self.devis = devis
        self.entreprise = entreprise
        self.adresse_entreprise = adresse_entreprise
        self.date = date
        self.client = client
        self.adresse_client = adresse_client
        self.code_postal_client = code_postal_client
        self.description = description
        self.montant_total = montant_total
        self.taux_tva = taux_tva
        self.total_ttc = total_ttc
        self.conditions = conditions
        self.debut_travaux = debut_travaux



    def __repr__(self):
        """ Méthode qui affiche toutes les infos d'un Devis """
        return (f"Devis(Devis={self.devis}, Entreprise={self.entreprise}, "
                f"Adresse Entreprise={self.adresse_entreprise}, Date={self.date}, "
                f"Client={self.client}, Adresse Client={self.adresse_client}, "
                f"Code Postal Client={self.code_postal_client}, Description={self.description}, "
                f"Montant Total={self.montant_total}, Taux TVA={self.taux_tva}, "
                f"Total TTC={self.total_ttc}, Conditions={self.conditions}, "
                f"Début Travaux={self.debut_travaux})")


