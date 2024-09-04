import chromadb
from sentence_transformers import SentenceTransformer
import config
import json
import logging






class VectorDataBase:
    """ Classe de la BDD Vectorielle / Stocke les données de l'entreprise """



    def __init__(self):
        """ Constructeur """
        # Initialisation du modèle d'Embedding :
        self.embedding_model = SentenceTransformer(config.VECTORIAL_BDD_MODEL)
        # Initialisation de la BDD Vectorielle :
        self.chroma_client = chromadb.Client()
        # Chargement du fichier de données de l'entreprise :
        self.load_commercial_context_dataset(config.COMPANY_COMMERCIAL_DATA)



    """ Configuration des logs. """
    logging.basicConfig(level=logging.INFO)



    def generate_embedding(self, text):
        """ Méthode qui transforme les données textes en Vecteur. """
        
        try:
            embedding = self.embedding_model.encode(text).tolist()
            return embedding
        
        except Exception as e:
            logging.error(f"Erreur lors de la génération de l'embedding : {str(e)}")
            raise ValueError(f"Erreur lors de la génération de l'embedding : {str(e)}") from e



    def populate_vectors(self, dataset):
        """ Méthode qui enregistre les vecteurs en BDD. """
        print("DATASET CHARGÉ DANS LA BDD VECTORIELLE : ", dataset)

        try:
            for i, item in enumerate(dataset):
                combined_text = f"{item['instruction']}. {item['context']}"
                try:
                    embeddings = self.generate_embedding(combined_text)
                    collection = self.chroma_client.get_or_create_collection(name="my_collection")
                    collection.add(embeddings=[embeddings], documents=[item['context']], ids=[f"id_{i}"])

                except Exception as e:
                    logging.error(f"Erreur lors de l'ajout du vecteur pour l'élément {i} : {str(e)}")
                    raise RuntimeError(f"Erreur inattendue lors de l'ajout du vecteur pour l'élément {i} : {str(e)}") from e
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la population des vecteurs : {str(e)}")
            raise RuntimeError(f"Erreur inattendue lors de la population des vecteurs : {str(e)}") from e



    def insert(self, embedding, metadata):
        """ Méthode qui insère un devis en BDD. """

        try:
            print("EMBEDDING : ", embedding)
            document = f"Devis: {metadata['Devis']}"
            collection = self.chroma_client.get_or_create_collection(name="my_collection")
            collection.add(embeddings=[embedding], documents=[document], ids=[metadata['Devis']])

        except Exception as e:
            logging.error(f"Erreur inattendue lors de l'insertion dans la base vectorielle : {str(e)}")
            raise RuntimeError(f"Erreur inattendue lors de l'insertion dans la base vectorielle : {str(e)}") from e



    def search_context(self, query):
        """ Méthode pour rechercher des vecteurs via une query. """

        try:
            query_embeddings = self.generate_embedding(query)
            collection = self.chroma_client.get_or_create_collection(name="my_collection")
            result = collection.query(query_embeddings=query_embeddings)
            return result
        
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la recherche du contexte : {str(e)}")
            raise RuntimeError(f"Erreur inattendue lors de la recherche du contexte : {str(e)}") from e



    def retrieve_all_data(self):
        """ Méthode pour récupérer toutes les données de la collection vectorielle. """
        try:
            # Accès à la collection
            collection = self.chroma_client.get_or_create_collection(name="my_collection")

            # Récupération de toutes les données dans la collection (assurez-vous que get() est supporté)
            result = collection.get()

            logging.info(f"Nombre total d'entrées récupérées : {len(result['ids'])}")
            return result
        
        except Exception as e:
            logging.error(f"Erreur inattendue lors de la récupération des données : {str(e)}")
            raise RuntimeError(f"Erreur inattendue lors de la récupération des données : {str(e)}") from e



    def load_commercial_context_dataset(self, dataset_path):
        """ Méthode pour charger les devis dans la BDD vectorielle. """

        try:
            # Chargement de chaque ligne du fichier jsonl :
            with open(dataset_path, 'r') as file:
                dataset = [json.loads(line) for line in file]
            # Chargement du dataset dans la BDD vectorielle :
            self.populate_vectors(dataset)
            logging.info(f"Dataset chargé et inséré dans la base vectorielle depuis {dataset_path}")

        except FileNotFoundError as fnfe:
            logging.error(f"Fichier non trouvé : {dataset_path}. Erreur : {fnfe}")
            raise FileNotFoundError(f"Fichier non trouvé : {dataset_path}. Erreur : {fnfe}") from fnfe
        except json.JSONDecodeError as jde:
            logging.error(f"Erreur lors de la lecture du fichier JSONL : {dataset_path}. Erreur : {jde}")
            raise ValueError(f"Erreur lors de la lecture du fichier JSONL : {jde}") from jde
        except Exception as e:
            logging.error(f"Erreur inattendue lors du chargement des devis : {str(e)}")
            raise RuntimeError(f"Erreur inattendue lors du chargement des devis : {str(e)}") from e

