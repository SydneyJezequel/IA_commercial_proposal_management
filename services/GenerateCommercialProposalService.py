from BO.Llm import Llm
import logging






class GenerateCommercialProposalService:
    """ Service qui génère une offre commercial en fonction des devis et information de notre entreprise """



    def __init__(self):
        """ Constructeur """
        # Instanciation du LLM :
        self.llm = Llm()



    """ Configuration des logs """
    logging.basicConfig(level=logging.INFO)



    def generate_commercial_proposal(self):
        """ Méthode qui génère la proposition commerciale. """

        try:
            proposal = self.llm.generate_commercial_proposal()
            return proposal
        
        except ConnectionError as ce:
            logging.error(f"Erreur de connexion : {str(ce)}")
            raise RuntimeError("Erreur de connexion. Veuillez réessayer plus tard.") from ce
        except ValueError as ve:
            logging.error(f"Erreur de valeur : {str(ve)}")
            raise ValueError("Erreur de valeur. Vérifiez les données d'entrée.") from ve
        except Exception as e:
            logging.error(f"Une erreur inattendue est survenue : {str(e)}")
            raise RuntimeError("Une erreur inattendue est survenue lors de la génération de la proposition.") from e

