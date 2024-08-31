from BO.Llm import Llm






class GenerateCommercialProposalService:
    """ Service qui génère une offre commercial en fonction des devis et information de notre entreprise """



    def __init__(self):
        """ Constructeur """
        # Instanciation du LLM :
        self.llm = Llm()


            
    def generate_commercial_proposal(self):
        """ Méthode qui génère la proposition commerciale """
        return self.llm.generate_commercial_proposal()

