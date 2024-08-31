from BO.Llm import Llm






class GenerateCommercialProposalService:
    """ Classe chargée de la génération d'une offre commercial en fonction des devis existants """




    """ ***************** Constructeur ***************** """

    def __init__(self):
        """ Constructeur """
        # Instanciation du LLM :
        self.llm = Llm()




    """ ***************** Méthodes ***************** """
            
    def generate_commercial_proposal(self):
        """ Méthode qui génère la proposition commerciale en fonction des devis concurrents et des informations de l'entreprise """
        return self.llm.generate_commercial_proposal()

