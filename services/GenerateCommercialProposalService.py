from BO.VectorDatabase import VectorDataBase






class GenerateCommercialProposalService:
    """ Classe chargée de la génération d'une offre commercial en fonction des devis existants """




    """ ***************** Constructeur ***************** """

    def __init__(self):
        """ Constructeur """
        # Bdd Vectorielle :
        self.vector_db = VectorDataBase()




    """ ***************** Méthodes ***************** """

    def generate_commercial_proposal(self):
        """ Méthode qui génère une offre commerciale en fonction des devis """
        print("Offre commerciale générée.")
        return "Offre commerciale générée."







    """
    def load_dataset_into_vector_store(self):
        # Chargement du dataset dans Chroma DB 
        try:
            self.vector_store.populate_vectors(self.embedded_dataset)
            print("dataset chargé dans le vector store. ")
            return True
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return False

            

    def get_llm_embedding_answer(self, input_question):
        # Méthode qui répond aux questions
        # Préparation des paramètres de la question :
        question = input_question.question
        # Récupération du context dans la BDD Vectorielle :
        context_response = self.vector_store.search_context(question)
        # Extraction du contexte de la réponse :
        context = "".join(context_response['documents'][0])
        print("CONTEXT : ", context)
        # Génération de la réponse :
        response = self.llm_model.generate_enriched_answer(question, context=context)
        return response
    """

