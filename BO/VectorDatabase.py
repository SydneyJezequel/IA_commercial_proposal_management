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
        # Chargement des données contenues dans les devis :
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")
        # Chargement du fichier de données de l'entreprise à partir du fichier "commercial_context_dataset" :
        self.load_commercial_context_dataset(config.COMPANY_COMMERCIAL_DATA)



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
        document = f"Devis: {metadata['Devis']}"
        self.collection.add(embeddings=[embedding], documents=[document], ids=[metadata['Devis']])









    # ******************************* NOUVELLE VERSION ******************************* #

    def search_context(self, query):
        """ Méthode pour rechercher des vecteurs à partir d'une requête """
        print("EXECUTION METHODE search_context()")
        print(" QUERY : ", query)
        query_embeddings = self.generate_embedding(query)
        return self.collection.query(query_embeddings=query_embeddings)

    # ******************************* NOUVELLE VERSION ******************************* #




    # ******************************* VERSION ACTUELLE ******************************* #
    """
    def search_context(self, query, n_results=1):
        # Méthode pour rechercher des vecteurs à partir d'une requête
        print("EXECUTION METHODE search_context()")
        print(" QUERY : ", query)
        print(" N RESULT : ", n_results)
        query_embeddings = self.generate_embedding(query)
        return self.collection.query(query_embeddings=query_embeddings, n_results=n_results)
    """
    # ******************************* VERSION ACTUELLE ******************************* #













    # ******************************* VERSION DE TEST ******************************* #
    def retrieve_all_documents(self):
        """ Récupérer tous les documents de la base de données vectorielle. """
        print("EXECUTION METHODE retrieve_all_documents()")
        
        # Récupérer tous les documents
        all_documents = self.collection.get_all_documents()  # Assurez-vous que cette méthode existe
        
        if all_documents:
            print("DOCUMENTS RECUPERES DE LA BDD : ", all_documents)
            # Traiter les documents si nécessaire
            return self.extract_relevant_data(all_documents)
        
        print("AUCUN DOCUMENT TROUVE.")
        return []
    # ******************************* VERSION DE TEST ******************************* #






    # ******************************* VERSION DE TEST ******************************* #
    """
    def display_text_from_vector(self, vector, model):
        # Méthode qui reconstitue et affiche le texte à partir d'un vecteur
        # Utiliser le modèle pour reconstruire le texte à partir du vecteur
        reconstructed_text = self.embedding_model.decode
        print("Texte reconstitué :")
        print(reconstructed_text)
    """
    # ******************************* VERSION DE TEST ******************************* #







































    # ******************************* NOUVELLES VERSIONS ******************************* #
    """ 
    def search_context(self, query, n_results=1):
        # Méthode pour rechercher des vecteurs à partir d'une requête
        print("EXECUTION METHODE search_context()")
        print(" QUERY : ", query)
        print(" N RESULT : ", n_results)
        # Générer des embeddings pour la requête
        query_embeddings = self.generate_embedding(query)
        # Formuler une requête spécifique pour récupérer les devis
        # (Peut nécessiter un ajustement selon votre structure de base de données)
        if "devis" in query.lower():  # Vérification si la requête concerne des devis
            results = self.collection.query(query_embeddings=query_embeddings, n_results=n_results)
            # Traitez les résultats pour s'assurer qu'ils contiennent les données nécessaires
            if results and results['documents']:
                return self.extract_relevant_data(results['documents'])
        return {}
    


    def extract_relevant_data(self, documents):
        # Extraire les informations pertinentes des documents récupérés.
        print("DEVIS RECUPERES EN BDD : ", documents)
        extracted_data = []
        for doc in documents:
            print("ITERATION SUR LES DOCUMENTS : ", doc)
            # Vérifiez si le document est une liste ou un format spécifique
            if isinstance(doc, list) and len(doc) > 0:
                # Si doc est une liste, accédez à son premier élément
                document_content = doc[0]  # Ici, `document_content` peut être une chaîne de caractères
                # Vous devez maintenant parser le contenu si c'est une chaîne
                extracted_data.append({
                    "Client": "Nom Client",  # Remplacez par un parsing si nécessaire
                    "Adresse Client": "Adresse Client",  # Remplacez par un parsing si nécessaire
                    "Code Postal Client": "Code Postal Client",  # Remplacez par un parsing si nécessaire
                    "Description": document_content,  # Contenu récupéré
                    "Montant Total": "Montant",  # Remplacez par un parsing si nécessaire
                    "Taux TVA": "Taux",  # Remplacez par un parsing si nécessaire
                    "Total TTC": "Total TTC",  # Remplacez par un parsing si nécessaire
                    "Début Travaux": "Date",  # Remplacez par un parsing si nécessaire
                    "Conditions": "Conditions"  # Remplacez par un parsing si nécessaire
                })
        print("DEVIS RECUPERES EN BDD POST TRAITEMENT : ", extracted_data)    
        return extracted_data
    """
    # ******************************* NOUVELLES VERSIONS ******************************* #





















    def load_commercial_context_dataset(self, dataset_path):
        """ Méthode pour charger et insérer les données du dataset dans la base vectorielle """
        try:
            print('EXECUTION METHODE load_commercial_context_dataset()')
            # dataset_path = "ressources/commercial_context_dataset.jsonl"  # Chemin relatif du fichier
            # dataset_path = config.COMPANY_COMMERCIAL_DATA
            with open(dataset_path, 'r') as file:
                dataset = [json.loads(line) for line in file]  # Charger chaque ligne du fichier jsonl
            # Charger les données dans la BDD vectorielle :
            self.populate_vectors(dataset)
            print(f"Dataset chargé et inséré dans la base vectorielle depuis {dataset_path}")
        except Exception as e:
            print(f"Erreur lors du chargement du dataset : {e}")






