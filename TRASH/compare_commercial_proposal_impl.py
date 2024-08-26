


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


""" Exécution de la méthode """
processed_image_path = preprocess_image(config.IMAGE_PATH)








""" **************** Extraction des informations des devis via un modèle OCR **************** """
import pytesseract
from PIL import Image


# Définir le chemin de l'exécutable Tesseract si nécessaire
pytesseract.pytesseract.tesseract_cmd =  '/usr/local/bin/tesseract'


""" Utilisation de Tesseract pour extraire le texte """
try:
    # Charger l'image pré-traitée :
    image = Image.open(processed_image_path)
    # Utiliser Tesseract pour extraire le texte
    extracted_text = pytesseract.image_to_string(image, lang='fra', config='--psm 6 --oem 3')
    print(" **************************** TEXTE BRUT **************************** ")
    print(extracted_text)
except pytesseract.TesseractError as e:
    print(f"Une erreur Tesseract s'est produite : {e}")
except Exception as e:
    print(f"Une erreur est survenue : {e}")







""" **************** Retraitement du devis avec le LLM **************** """
from llm import Model



""" Initialisation du modèle """
llm = Model()


""" Préparation du prompt """

question = "Peux-tu m'indiquer le montant total du devis et l'entreprise qui l'émet ?" 
prompt = question + extracted_text

""" Utilisation du modèle """
answer = llm.generate_answer(prompt)
print("answer : ", answer)


















































""" **************** Comparer les devis **************** """










