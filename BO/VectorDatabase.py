import chromadb
from sentence_transformers import SentenceTransformer
import config
import json






class VectorDataBase:
    """ BDD Vectorielle """



    def __init__(self):
        """ Constructeur """
        # Initialisation du modèle d'Embedding :
        self.embedding_model = SentenceTransformer(config.VECTORIAL_BDD_MODEL)
        # Initialisation de la BDD Vectorielle :
        self.chroma_client = chromadb.Client()
        # Chargement du fichier de données de l'entreprise à partir du fichier "commercial_context_dataset" :
        self.load_commercial_context_dataset(config.COMPANY_COMMERCIAL_DATA)



    def generate_embedding(self, text):
        """ Méthode qui transforme le texte en Vecteur """
        return self.embedding_model.encode(text).tolist()



    def populate_vectors(self, dataset):
        """ Méthode qui enregistre les vecteurs en BDD """
        print("EXECUTION METHODE populate_vectors()")      
        print("DATASET CHARGE DANS LA BDD VECTORIELLE : ", dataset)
        for i, item in enumerate(dataset):
            combined_text = f"{item['instruction']}. {item['context']}"
            embeddings = self.generate_embedding(combined_text)
            collection = self.chroma_client.get_or_create_collection(name="my_collection")
            collection.add(embeddings=[embeddings], documents=[item['context']], ids=[f"id_{i}"])



    def insert(self, embedding, metadata):
        print("EXECUTION METHODE Insert()")
        print("EMBEDDING : ", embedding)
        document = f"Devis: {metadata['Devis']}"
        collection = self.chroma_client.get_or_create_collection(name="my_collection")
        collection.add(embeddings=[embedding], documents=[document], ids=[metadata['Devis']])



    def search_context(self, query):
        """ Méthode pour rechercher des vecteurs à partir d'une requête """
        print("EXECUTION METHODE search_context()")
        print(" QUERY : ", query)
        query_embeddings = self.generate_embedding(query)
        collection = self.chroma_client.get_or_create_collection(name="my_collection")
        return collection.query(query_embeddings=query_embeddings)



    def load_commercial_context_dataset(self, dataset_path):
        """ Méthode pour charger et insérer les données du dataset dans la base vectorielle """
        try:
            print('EXECUTION METHODE load_commercial_context_dataset()')
            with open(dataset_path, 'r') as file:
                dataset = [json.loads(line) for line in file]  # Charger chaque ligne du fichier jsonl
            # Charger les données dans la BDD vectorielle :
            self.populate_vectors(dataset)
            print(f"Dataset chargé et inséré dans la base vectorielle depuis {dataset_path}")
        except Exception as e:
            print(f"Erreur lors du chargement du dataset : {e}")

