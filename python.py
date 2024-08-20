
""" ******************** Manipulations en Python ******************** """

"""
print("Hello World ! ")

a = 1
b = 2

c = a + b
print(f'{c}')
"""




























""" ******************** Réflexion sur la comparaison de fiches produits clients ******************** """






#  ************** Chargement des Tokenisers et Modèles  ************** #

from transformers import BertTokenizer, TFBertModel
import tensorflow as tf
import faiss
import numpy as np

# Charger le tokenizer et le modèle BERT pour générer des embeddings
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertModel.from_pretrained('bert-base-uncased')






# ************** Génération des Embeddings et Stockage dans la BDD Vectorielle  **************  #

def generate_embedding(text):
    # Prétraitement du texte pour le modèle BERT
    inputs = tokenizer(text, return_tensors='tf', max_length=512, truncation=True, padding=True)
    outputs = model(**inputs)
    # Retourner le vecteur du token [CLS]
    return outputs.last_hidden_state[:, 0, :].numpy()

# Initialiser la base de données vectorielle FAISS
d = 768  # Dimension des embeddings BERT
index = faiss.IndexFlatL2(d)  # Index avec la distance euclidienne
product_db = []  # Stocker les descriptions de produits pour les retrouver par leur ID

# Charger les fiches produits de l'entreprise et des concurrents
fiches_produits = [
    {"nom": "Produit_A", "description": "Notre produit propose un écran ultra haute résolution, une batterie plus puissante."},
    {"nom": "Produit_B", "description": "Le produit concurrent est doté d'un écran haute résolution et d'une batterie longue durée."},
    # Ajoutez d'autres fiches produits ici
]

# Générer les embeddings et les ajouter à la BDD Vectorielle
for fiche in fiches_produits:
    embedding = generate_embedding(fiche["description"])
    index.add(embedding)
    product_db.append(fiche)

# Indexer pour des recherches efficaces
faiss.normalize_L2(index.reconstruct_n(0, index.ntotal))







# ************** Comparaison des Fiches Produits et Génération de l'Argumentaire ************** #

def compare_and_generate_argument(product_name, product_description):
    # Générer l'embedding de la fiche produit à comparer
    embedding = generate_embedding(product_description)
    
    # Rechercher le produit le plus proche dans la BDD vectorielle
    D, I = index.search(embedding, k=1)
    closest_product_id = I[0][0]
    closest_product = product_db[closest_product_id]
    
    arguments = []
    
    # Comparer chaque caractéristique
    for key, value in closest_product["caracteristiques"].items():
        if key in product_db[0]["caracteristiques"]:
            if product_db[0]["caracteristiques"][key] != value:
                if key == "prix":
                    if float(product_db[0]["caracteristiques"][key].replace('€', '')) > float(value.replace('€', '')):
                        arguments.append(f"Notre produit est un peu plus cher ({product_db[0]['caracteristiques'][key]}) mais offre de meilleures fonctionnalités.")
                    else:
                        arguments.append(f"Notre produit est plus compétitif en prix ({product_db[0]['caracteristiques'][key]}) tout en maintenant des fonctionnalités de haute qualité.")
                else:
                    arguments.append(f"Notre {key} est meilleur : {product_db[0]['caracteristiques'][key]} contre {value} du produit concurrent.")
    
    # Si aucune différence n'est détectée
    if not arguments:
        arguments.append("Notre produit est comparable au concurrent mais offre une meilleure expérience globale.")
    
    return arguments

# Exemple d'utilisation
notre_fiche_produit = {
    "nom": "Produit_A",
    "description": "Notre produit propose un écran ultra haute résolution, une batterie plus puissante."
}

# Générer la liste d'arguments
arguments = compare_and_generate_argument(notre_fiche_produit["nom"], notre_fiche_produit["description"])
for arg in arguments:
    print(arg)

