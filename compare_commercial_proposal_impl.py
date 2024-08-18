






""" **************** Extraction des informations des devis via un modèle OCR **************** """
import config
import pytesseract
from PIL import Image

# Définir le chemin de l'exécutable Tesseract si nécessaire
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'


# Utiliser Tesseract pour extraire le texte
try:
    # Charger l'image à partir du chemin spécifié
    image = Image.open(config.IMAGE_PATH)
    
    # Utiliser Tesseract pour extraire le texte
    extracted_text = pytesseract.image_to_string(image, lang='fra')
    print(extracted_text)
except pytesseract.TesseractError as e:
    print(f"Une erreur Tesseract s'est produite : {e}")
except Exception as e:
    print(f"Une erreur est survenue : {e}")





""" **************** Vérifier les informations des devis **************** """

""" 
import spacy

# Charger un modèle de langage français de spaCy
nlp = spacy.load("fr_core_news_md")

# Appliquer le modèle NLP sur le texte extrait
doc = nlp(extracted_text)

# Extraire les informations :
for ent in doc.ents:
    print(ent.label_, ent.text)
"""






""" **************** Comparer les devis **************** """

"""
import pytesseract
from PIL import Image
import spacy

def extract_text_from_image(image_path):
    # Charger l'image
    image = Image.open(image_path)
    # Extraire le texte avec Tesseract OCR
    return pytesseract.image_to_string(image, lang='fra')

def extract_info_from_text(text):
    # Charger le modèle spaCy
    nlp = spacy.load("fr_core_news_md")
    doc = nlp(text)
    data = {}
    # Extraire les informations clés
    for ent in doc.ents:
        data[ent.label_] = ent.text
    return data

# Exemple d'utilisation
image_path = 'devis_image.jpg'
text = extract_text_from_image(image_path)
info = extract_info_from_text(text)
print(info)
"""












































""" 
==> REFLEXION :
Le code que vous avez partagé est principalement conçu pour effectuer des tâches de "Visual Question Answering" (VQA), qui implique de répondre à des questions sur des images. Cela signifie qu'il n'est pas directement adapté pour comparer deux devis et déterminer lequel a le meilleur prix, car cela nécessite une comparaison textuelle ou numérique entre deux ensembles de données textuelles (les devis) plutôt qu'une interprétation visuelle.

Cependant, vous pouvez adapter le pipeline VQA ou utiliser d'autres techniques d'IA pour comparer deux devis. Voici quelques étapes pour une solution possible :
1. Modifier l'Entrée Textuelle :
Plutôt que de traiter des images, vous pourriez concevoir un modèle de traitement de texte pour comprendre et comparer deux devis textuels.
Pour cela, vous pouvez utiliser un modèle de traitement de langage naturel (NLP) comme GPT-3 ou T5, qui serait entraîné à comparer les valeurs numériques dans des textes.
2. Préparer les Données :
Convertissez les devis en textes structurés.
Exemple :
Devis 1 : "Entreprise: A, Quantité: 100 m², Prix unitaire: 15€/m², Total: 1500€"
Devis 2 : "Entreprise: B, Quantité: 100 m², Prix unitaire: 12€/m², Total: 1200€"
Formulez une question : "Lequel des deux devis a le meilleur prix ?"
3. Utilisation d'un Modèle NLP :
Vous pouvez utiliser un modèle pré-entraîné comme GPT pour comparer ces devis :
Exemple de question : "Entre ces deux devis, lequel offre le meilleur prix pour 100 m² ?"
4. Pipeline de Comparaison :
Si vous utilisez un modèle T5 ou GPT :
Préparez une entrée qui inclut les deux devis.
Demandez au modèle de comparer les deux et de choisir le meilleur.
Le modèle devrait répondre avec le devis ayant le prix le plus bas.
5. Entraînement Spécifique
Si les devis sont très complexes, vous pourriez envisager de fine-tuner un modèle sur un dataset spécifique de comparaisons de devis pour améliorer la précision.
Conclusion
Le code que vous avez partagé pourrait être adapté pour cette tâche, mais il nécessite des ajustements considérables. La stratégie la plus simple est de s'orienter vers un modèle NLP capable de traiter et comparer des textes pour déterminer lequel des deux devis est le plus économique. Vous pourriez également utiliser un modèle de type text2text pour cette comparaison, ou entraîner un modèle spécifique à partir d'un dataset de devis comparés.
"""









