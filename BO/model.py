from sentence_transformers import SentenceTransformer
import config
from monsterapi import client






class Model:
    """ Classe du Modèle """


    def __init__(self):
        """ Constructeur """
        # Définition du modèle :
        self.model_name = config.MODEL_NAME_FALCON7B
        # Initialisation des pipeline, tokenizer et modèle :
        self.monster_client = self.initialize_model()



    def initialize_model(self):
        """ Méthode qui initialise le modèle """
        # Initialisation du client MonsterAPI avec la clé API :
        monster_api_key = config.MONSTER_API_KEY
        monster_client = client(monster_api_key)
        # Renvoi du pipeline, du tokenizer et du client MonsterAPI :
        return monster_client
    













""" 
    def __init__(self):
        # Constructeur
        self.model = SentenceTransformer(config.MODEL_NAME)
"""         












