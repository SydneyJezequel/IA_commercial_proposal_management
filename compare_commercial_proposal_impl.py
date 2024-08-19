


""" **************** Pré-traitement de l'image **************** """
import cv2
import config



def preprocess_image(image_path):
    """ Méthode qui pré-traite l'image """

    # Charger l'image
    img = cv2.imread(image_path)

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Augmenter le contraste en appliquant un filtre de seuil
    _, thresh_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Sauvegarder et retourner le chemin de l'image prétraitée
    processed_image_path = 'processed_image.png'
    cv2.imwrite(processed_image_path, thresh_img)
    return processed_image_path



processed_image_path = preprocess_image(config.IMAGE_PATH)








""" **************** Extraction des informations des devis via un modèle OCR **************** """
import pytesseract
from PIL import Image

# Définir le chemin de l'exécutable Tesseract si nécessaire
pytesseract.pytesseract.tesseract_cmd =  '/usr/local/bin/tesseract'


# Utiliser Tesseract pour extraire le texte
try:

    # Charger l'image pré-traitée :
    image = Image.open(processed_image_path)

    # Utiliser Tesseract pour extraire le texte
    extracted_text = pytesseract.image_to_string(image, lang='fra', config='--psm 6 --oem 3')
    print(" **************************** TEXTE BRUT **************************** ")
    print(extracted_text)

    # Nettoyage du texte extrait pour améliorer la reconnaissance des chiffres
    # cleaned_text = extracted_text.replace('€', '€ ')
    # cleaned_text = cleaned_text.replace('0', '0')
    # print(" **************************** TEXTE NETTOYÉ **************************** ")
    # print(cleaned_text)

except pytesseract.TesseractError as e:
    print(f"Une erreur Tesseract s'est produite : {e}")
except Exception as e:
    print(f"Une erreur est survenue : {e}")







""" **************** Retraitement du devis avec le LLM **************** """
from BO.model import Model



# Initialisation du modèle :
llm = Model()



def refine_text(text):
    """ Méthode pour rafiner le texte en utilisant Falcon 7B Instruct """
    
    # Préparation du prompt pour Falcon 7B
    prompt = f"Corrigez et reformulez ce texte : {text}"
    
    # Initialisation des paramètres de l'input
    top_k = 15
    top_p = 0.1
    temp = 0.1
    max_length = 256
    beam_size = 1
    
    # Préparation des données à envoyer à l'API
    input_data = {
        'prompt': prompt,
        'top_k': top_k,
        'top_p': top_p,
        'temp': temp,
        'max_length': max_length,
        'beam_size': beam_size,
    }

    try:
        # Génération des réponses avec le modèle Falcon 7B :
        output = llm.monster_client.generate(llm.model_name, input_data)
        print("OUTPUT : ", output)
        print("TYPE OUTPUT : ", type(output))
        
        # Récupération et affichage du texte généré :
        generated_text = output[0]['generated_text']
        print("Texte raffiné : ", generated_text)
        return generated_text
    
    except Exception as e:
        print(f"Erreur lors de la génération de texte : {e}")
        return None




# Exemple d'utilisation de la fonction refine_text
refined_text = refine_text(extracted_text)
print("refined_text : ", refined_text)










































































































"""
import openai

def refine_text(text):
    response = openai.Completion.create(
        engine="gpt-4",  # Choisissez le modèle approprié
        prompt=f"Corrigez et reformulez ce texte : {text}",
        max_tokens=500
    )
    return response.choices[0].text.strip()

refined_text = refine_text(extracted_text)
"""










""" **************** Vérifier les informations des devis **************** """


import spacy
import fr_core_news_md


try:
    # Charger un modèle de langage français de spaCy
    nlp = fr_core_news_md.load()

    # Appliquer le modèle NLP sur le texte extrait
    doc = nlp(extracted_text)

    # Extraire les informations :
    print(" **************************** INFORMATIONS RECUPEREES **************************** ")
    for ent in doc.ents:
        print(ent.label_, ent.text)
except spacy.errors as e:
    print(f"Une erreur Spacy s'est produite : {e}")
except Exception as e:
    print(f"Une erreur est survenue : {e}")






""" **************** Comparer les devis **************** """







































































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



























