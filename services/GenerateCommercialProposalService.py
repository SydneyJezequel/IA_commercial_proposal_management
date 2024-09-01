from BO.Llm import Llm






class GenerateCommercialProposalService:
    """ Service qui génère une offre commercial en fonction des devis et information de notre entreprise """



    def __init__(self):
        """ Constructeur """
        # Instanciation du LLM :
        self.llm = Llm()


            
    def generate_commercial_proposal(self):
        """ Méthode qui génère la proposition commerciale. """

        try:
            proposal = self.llm.generate_commercial_proposal()
            return proposal
        
        except ConnectionError as ce:
            raise RuntimeError("Erreur de connexion. Veuillez réessayer plus tard.")
        except ValueError as ve:
            raise ValueError("Erreur de valeur. Vérifiez les données d'entrée.")
        except Exception as e:
            raise RuntimeError("Une erreur inconnue est survenue lors de la génération de la proposition.")

