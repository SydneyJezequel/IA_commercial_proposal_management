

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
        """ Méthode qui affiche les infos clés d'un Devis """
        return f"Devis(Devis={self.devis}, Entreprise={self.entreprise}, Montant={self.total_ttc})"

