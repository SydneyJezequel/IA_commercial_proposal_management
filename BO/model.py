from sentence_transformers import SentenceTransformer
import config






class Model:
    """ Classe du Modèle """



    def __init__(self):
        """ Constructeur """
        self.model = SentenceTransformer(config.MODEL_NAME)

