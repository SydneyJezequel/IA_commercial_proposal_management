import pytesseract
from PIL import Image
import cv2
from spellchecker import SpellChecker
import os
import config
import logging






class QuotationDataExtractorService:
    """ Service qui récupère les données dans les devis """



    def __init__(self):
        """ Constructeur """
        # Emplacements des devis :
        self.image_paths = [os.path.join(config.QUOTATIONS_FILES_PATH, image) for image in config.QUOTATIONS_FILES_LIST]
        # Contenu des devis :
        self.extracted_texts = []



    """ Configuration des logs """
    logging.basicConfig(level=logging.INFO)



    def preprocess_image(self, image_path):
        """ Méthode qui pré-traite l'image et la sauvegarde dans le répertoire de sortie. """
        logging.info(f"image_path for image to preprocess : {image_path}")

        try:
            # Lecture de l'image en niveaux de gris pour simplifier son traitement :
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError(f"L'image à l'emplacement {image_path} n'a pas pu être chargée.")
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
            logging.info(f"processed_image_path : {processed_image_path}")
            return processed_image_path
        
        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors du traitement de l'image {image_path}: {str(e)}")
            return None


    
    def process_quotations(self):
        """ Méthode qui récupère les informations de chaque devis. """

        for image_path in self.image_paths:

            try:
                text = self.extract_text(image_path)
                self.extracted_texts.append(text)

            except Exception as e:
                logging.error(f"Une erreur inattendue s'est produite lors de l'extraction de texte pour l'image {image_path}: {str(e)}")
                raise RuntimeError(f"Une erreur inattendue s'est produite lors de l'extraction de texte pour l'image {image_path}.") from e



    def extract_text(self, image_path):
        """ Méthode qui extrait le texte contenu dans chaque devis. """

        try:
            processed_image_path = self.preprocess_image(image_path)
            image = Image.open(processed_image_path)
            extracted_text = pytesseract.image_to_string(image, lang='fra', config='--psm 3 --oem 3')
            clean_text = self.clean_extracted_text(extracted_text)
            logging.info(f"clean_extracted_text : {clean_text}")
            return clean_text
        
        except pytesseract.TesseractError as e:
            logging.error(f"Erreur Tesseract : {str(e)}")
            raise RuntimeError(f"Erreur Tesseract : {str(e)}") from e
        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors du traitement de l'image {image_path} : {str(e)}")
            raise RuntimeError(f"Une erreur inattendue s'est produite lors du traitement de l'image {image_path} : {str(e)}") from e



    def clean_extracted_text(self, text):
        """ Méthode qui corrige le texte extrait. """

        try:
            spell = SpellChecker(language='fr') 
            cleaned_text = []
            for word in text.split():
                corrected_word = spell.correction(word)
                cleaned_text.append(corrected_word if corrected_word else word)
            return ' '.join(cleaned_text)
        
        except Exception as e:
            logging.error(f"Une erreur inattendue s'est produite lors de la correction du texte : {str(e)}")
            return text

