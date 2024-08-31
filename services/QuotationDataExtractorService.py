import pytesseract
from PIL import Image
import cv2
from spellchecker import SpellChecker
import os
import config






class QuotationDataExtractorService:
    """ Service qui récupère les données dans les devis """



    def __init__(self):
        """ Constructeur """
        # Emplacements des devis :
        self.image_paths = [os.path.join(config.QUOTATIONS_FILES_PATH, image) for image in config.QUOTATIONS_FILES_LIST]
        # Contenu des devis :
        self.extracted_texts = []



    def preprocess_image(self, image_path):
        """ Méthode qui pré-traite l'image et la sauvegarde dans le répertoire de sortie """
        print("IMAGE_PATH IN PREPROCESS_IMAGE : ", image_path)
        # Lecture de l'image en niveaux de gris pour simplifier son traitement :
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Amélioration du contraste de l'image :
        img = cv2.equalizeHist(img)
        # Réduction du bruit de l'image :
        img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        # Division de l'image en noir et blanc :
        thresh_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # Définir le chemin de la nouvelle image obtenue :
        processed_image_path = os.path.join(config.PROCESSED_QUOTATIONS_FILES_PATH, os.path.basename(image_path))
        # Sauvegarde de l'image traitée :
        cv2.imwrite(processed_image_path, thresh_img)
        print("processed_image_path : ", processed_image_path)
        return processed_image_path


    
    def process_quotations(self):
        """ Méthode qui récupère les informations de chaque devis """
        print("Chargement des informations de chaque devis dans self.extracted_texts() ")
        for image_path in self.image_paths:
            text = self.extract_text(image_path)
            self.extracted_texts.append(text)



    def extract_text(self, image_path):
        """ Méthode qui extrait le texte contenu dans chaque devis """
        try:
            processed_image_path = self.preprocess_image(image_path)
            image = Image.open(processed_image_path)
            extracted_text = pytesseract.image_to_string(image, lang='fra', config='--psm 3 --oem 3')
            clean_text = self.clean_extracted_text(extracted_text)
            print("clean_extracted_text :", clean_text)
            return clean_text
        except pytesseract.TesseractError as e:
            print(f"Une erreur Tesseract s'est produite : {e}")
        except Exception as e:
            print(f"Une erreur est survenue lors du traitement de {image_path} : {e}")
        return ""



    def clean_extracted_text(self, text):
        """ Méthode qui corrige le texte extrait """
        spell = SpellChecker(language='fr') 
        cleaned_text = []
        for word in text.split():
            corrected_word = spell.correction(word)
            cleaned_text.append(corrected_word if corrected_word else word)
        return ' '.join(cleaned_text)

