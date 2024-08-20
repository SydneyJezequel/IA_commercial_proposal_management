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
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Utiliser Tesseract pour extraire le texte
try:
    # Charger l'image pré-traitée :
    image = Image.open(processed_image_path)

    # Utiliser Tesseract pour extraire le texte
    extracted_text = pytesseract.image_to_string(image, lang='fra', config='--psm 6 --oem 3')
    print(" **************************** TEXTE BRUT **************************** ")
    print(extracted_text)

    """ **************** Nettoyage et extraction des montants **************** """
    import re
    import spacy
    import fr_core_news_md

    # Nettoyage manuel du texte extrait
    cleaned_text = extracted_text.replace('TotlH.T', 'Total H.T')
    cleaned_text = cleaned_text.replace('Té', 'Téléphone')
    cleaned_text = cleaned_text.replace('Esail', 'Email')
    cleaned_text = cleaned_text.replace('Bamai.com', 'Bomail.com')
    cleaned_text = cleaned_text.replace('Sito', 'Site')
    cleaned_text = cleaned_text.replace('Aéressé', 'Adressé')
    cleaned_text = cleaned_text.replace('Chamore', 'Chambre')
    cleaned_text = cleaned_text.replace('€', '€ ')
    cleaned_text = cleaned_text.replace('0', '0')
    
    print(" **************************** TEXTE NETTOYÉ **************************** ")
    print(cleaned_text)

    # Extraction des montants avec regex
    montants = re.findall(r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?\s*€', cleaned_text)
    print("Montants détectés :", montants)

    # Chargement et application du modèle SpaCy
    nlp = fr_core_news_md.load()
    doc = nlp(cleaned_text)

    # Organisation des informations extraites
    informations = {}

    for ent in doc.ents:
        if ent.label_ not in informations:
            informations[ent.label_] = []
        informations[ent.label_].append(ent.text)

    # Ajout des montants dans les informations
    informations['MONTANTS'] = montants

    # Affichage des informations extraites
    print(" **************************** INFORMATIONS RECUPEREES **************************** ")
    for label, texts in informations.items():
        print(f"{label}: {texts}")

except pytesseract.TesseractError as e:
    print(f"Une erreur Tesseract s'est produite : {e}")
except Exception as e:
    print(f"Une erreur est survenue : {e}")
