import chromadb
from sentence_transformers import SentenceTransformer
import config






class VectorDataBase:
    """ BDD Vectorielle """



    def __init__(self):
        """ Constructeur """
        # Initialisation du modèle d'Embedding :
        self.embedding_model = SentenceTransformer(config.VECTORIAL_BDD_MODEL)
        self.chroma_client = chromadb.Client()



    def generate_embedding(self, text):
        """ Méthode qui transforme le texte en Vecteur """
        print("EXECUTION METHODE generate_embedding()")
        print(" TEXT : ", text)
        return self.embedding_model.encode(text).tolist()



    def populate_vectors(self, dataset):
        """ Méthode qui enregistre les vecteurs en BDD """
        print("EXECUTION METHODE populate_vectors()")      
        print("DATASET : ", dataset)
        for i, item in enumerate(dataset):
            combined_text = f"{item['instruction']}. {item['context']}"
            embeddings = self.generate_embedding(combined_text)
            self.collection.add(embeddings=[embeddings], documents=[item['context']], ids=[f"id_{i}"])



    def insert(self, embedding, metadata):
        print("EXECUTION METHODE Insert()")
        print("EMBEDDING : ", embedding)
        print("METADATA : ", metadata)
        """ Méthode pour insérer un embedding dans la collection avec des métadonnées """
        self.collection.add(embeddings=[embedding], documents=[metadata["Devis"]], metadata=metadata)



    def search_context(self, query, n_results=1):
        """ Méthode pour rechercher des vecteurs à partir d'une requête """
        print("EXECUTION METHODE search_context()")
        print(" QUERY : ", query)
        print(" N RESULT : ", n_results)
        query_embeddings = self.generate_embedding(query)
        return self.collection.query(query_embeddings=query_embeddings, n_results=n_results)
