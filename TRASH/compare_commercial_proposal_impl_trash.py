from BO.model import Model






""" ******************************************************************************** """
""" ******************************* LISTE DES ETAPES ******************************* """
""" ******************************************************************************** """

"""
Etapes de la fonctionnalité :
1- Etape 1 : Traitement du besoin :
	1.1- Transformer la spec (le besoin) en liste de critères. 
	1.2- Vectoriser cette liste.
2- Etape 2 : Traitement des offres : 
	2.1- Transformer les offres en liste de critères.
	2.2- Vectoriser ces listes.
3- Etape 3 : Synthèse des points forts / faibles des offres avec classement.
4- Etape 4 : Générer un argumentaire de vente pour une des offres pour la positionner par rapport aux autres.
"""




















""" ***************************************************************************************** """
""" ******************************* IMPLEMENTATION DES ETAPES ******************************* """
""" ***************************************************************************************** """


llm = Model()






""" ******************* Étape 1 : Traitement du besoin ******************* """


def extract_criteria_from_spec(spec_text):
    """ Méthode qui renvoie la liste des critères du besoin """
    prompt = f"Voici un besoin : {spec_text}. Quels sont les critères clés à retenir ?"
    response = llm.generate(prompt)  # LLM générant la liste de critères
    return response.split('\n')  # Assume que chaque critère est séparé par une nouvelle ligne


from sentence_transformers import SentenceTransformer

def vectorize_criteria(criteria_list):
    """ Méthode qui vectorise les critères de la spéc """
    vectors = llm.encode(criteria_list)
    return vectors









""" ******************* Étape 2 : Traitement des offres ******************* """


def extract_criteria_from_offer(offer_text):
    """ Méthode qui extrait les critères d'une offre """
    prompt = f"Voici une offre : {offer_text}. Quels sont les critères clés de cette offre ?"
    response = llm.generate(prompt)
    return response.split('\n')


def vectorize_offers(offers):
    """ Méthode qui vectorise les critères des offres """
    vectors = [vectorize_criteria(extract_criteria_from_offer(offer)) for offer in offers]
    return vectors






""" ******************* Étape 3 : Synthèse des points forts / faibles des offres avec classement ******************* """

def rank_offers(need_vectors, offer_vectors):
    """ Méthode qui compare les vecteurs de l'offres avec ceux du besoin """
    rankings = []
    for offer_vector in offer_vectors:
        similarity_score = calculate_similarity(need_vectors, offer_vector) 
        rankings.append(similarity_score)
    # Classement des offres du meilleur au moins bon :
    return sorted(rankings, reverse=True) 


def compare_offer_with_need(offer_criteria, need_criteria):
    """ Méthode qui identifie les points forts et les points faibles de l'offre """
    strengths = []
    weaknesses = []
    for offer, need in zip(offer_criteria, need_criteria):
        if is_stronger(offer, need):
            strengths.append(offer)
        else:
            weaknesses.append(offer)
    return strengths, weaknesses



# Méthodes appelées :

import numpy as np

def calculate_similarity(need_vectors, offer_vector):
    """ Méthode qui calcule la similarité cosinus entre un ensemble de vecteurs de besoin et un vecteur d'offre. """
    # Moyenne des vecteurs du besoin pour obtenir un vecteur représentatif :
    mean_need_vector = np.mean(need_vectors, axis=0)
    # Calcul de la similarité cosinus :
    cosine_similarity = np.dot(mean_need_vector, offer_vector) / (np.linalg.norm(mean_need_vector) * np.linalg.norm(offer_vector))
    return cosine_similarity


def is_stronger(offer, need):
    """ Méthodes qui compare 2 critères (offre vs besoin) pour déterminer l'offre la plus forte. """
    # Comparaison simple basée sur un score ou une valeur numérique
    # Si l'offre est meilleure ou égale au besoin, elle est considérée plus forte.
    # Exemples de logique simple, vous pourriez avoir une logique plus complexe :
    if isinstance(offer, (int, float)) and isinstance(need, (int, float)):
        return offer >= need  # L'offre est plus forte si elle est supérieure ou égale au besoin
    # Comparaison textuelle (en supposant que les critères peuvent être des textes comparables)
    if isinstance(offer, str) and isinstance(need, str):
        return offer.lower() >= need.lower()  # Comparaison lexicale simple
    # Si les critères ne sont pas comparables directement
    return False







""" ******************* Étape 4 : Générer un argumentaire de vente ******************* """

def generate_sales_pitch(offer, strengths, weaknesses):
    """ Méthode qui génère l'argumentaire commercial """
    prompt = f"En considérant les points forts : {strengths} et les points faibles : {weaknesses} de l'offre, génère un argumentaire pour positionner cette offre par rapport aux autres."
    pitch = llm.generate(prompt)
    return pitch















"""
CONSEILS POUR LA BDD VECTORIELLE ET LE LLM A UTILISER :

1 / BDD VECTORIELLE :
==> PINECONE :
Avantages :
-Scalabilité : Pinecone est conçu pour gérer de grands volumes de données vectorielles, offrant une scalabilité quasi illimitée.
-Recherche rapide : Il offre des performances de recherche rapide et précise sur les vecteurs, même à grande échelle.
-Intégration facile : API conviviale avec une intégration facile dans des applications Python.
-Mises à jour en temps réel : Permet des insertions et mises à jour de vecteurs en temps réel.

==> WEAVIATE :
Avantages :
-Open-source : Weaviate est open-source, ce qui permet une personnalisation complète et une transparence totale.
-Modèles intégrés : Il prend en charge l'intégration de divers modèles d'encodage de texte et autres types de données.
-GraphQL API : Offre une API GraphQL puissante pour les requêtes complexes.



2 / LLM :
==> Sentence Transformers (SBERT) :
Avantages :
-Haute qualité des embeddings : Produit des embeddings de phrases de haute qualité, particulièrement adaptés aux tâches de similarité sémantique.
-Vitesse et efficacité : Le modèle est optimisé pour une utilisation rapide tout en maintenant une précision élevée.
-Facilité d'intégration : Peut être utilisé avec des frameworks populaires comme Hugging Face Transformers, et il est facile à intégrer avec les bases de données vectorielles comme Pinecone ou Weaviate.

==>  OpenAI Embeddings (text-embedding-ada-002) :
Avantages :
-Qualité des embeddings : Embeddings de très haute qualité pour les applications de recherche sémantique.
-Accès API : Disponible via une API facile à utiliser avec un support natif pour l'intégration avec Pinecone.
-Support multi-langue : Efficace sur plusieurs langues, ce qui est utile si votre application nécessite un support linguistique étendu.
"""








"""
CONSEILS POUR LE DEPLOIEMENT ET L'INTEGRATION :
- API RESTful : Créez une API REST qui permet aux utilisateurs de soumettre des spécifications et des offres, puis renvoie les résultats des étapes ci-dessus.
- Gestion des données : Utilisez une base de données vectorielle pour stocker et gérer les vecteurs des critères.
- Performance : En fonction de la taille des données, envisagez d'optimiser les requêtes et le stockage des vecteurs.
"""







