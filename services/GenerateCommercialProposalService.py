from BO.VectorDatabase import VectorDataBase
from BO.Llm import Llm






class GenerateCommercialProposalService:
    """ Classe chargée de la génération d'une offre commercial en fonction des devis existants """




    """ ***************** Constructeur ***************** """

    def __init__(self):
        """ Constructeur """
        # Instanciation de la BDD Vectorielle :
        self.vector_db = VectorDataBase()
        # Instanciation du LLM :
        self.llm = Llm()




    """ ***************** Méthodes ***************** """

    def test(self):
        """ Méthode qui génère une offre commerciale en fonction des devis """
        print("Offre commerciale générée.")
        return "Offre commerciale générée."

            

    def generate_commercial_proposal(self):
        """ Méthode qui génère la proposition commerciale en fonction des devis concurrents et des informations de l'entreprise """
        return self.llm.generate_commercial_proposal()

