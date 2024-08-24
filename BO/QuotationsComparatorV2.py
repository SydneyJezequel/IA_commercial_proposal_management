import re
import pytesseract
from PIL import Image
import cv2
from BO.VectorDatabase import VectorDataBase






class QuotationsComparatorV2:
    """ Classe chargée du traitement et de la comparaison des devis """





    """ ***************** Constructeur ***************** """

    def __init__(self, image_paths):
        """ Constructeur """
        # Emplacements des images :
        self.image_paths = image_paths
        # Contenu des devis :
        # self.processed_texts = []
        self.extracted_texts = []
        # Liste des informations sur les devis :
        self.devis_data = [] 
        # Bdd Vectorielle :
        self.vector_db = VectorDataBase()






    """ ***************** Méthode en charge du prétraitement et de l'extraction du texte des devis ***************** """

    def preprocess_image(self, image_path):
        """ Méthode qui pré-traite l'image """
        print("IMAGE_PATH IN PREPROCESS_IMAGE : ", image_path)
        img = cv2.imread(image_path, 1)
        print("img : ", img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        processed_image_path = image_path
        cv2.imwrite(processed_image_path, thresh_img)
        print("processed_image_path : ", processed_image_path)
        return processed_image_path

    """
    def preprocess_image(self, image_path):
        # Méthode qui pré-traite l'image
        print("IMAGE_PATH IN PREPROCESS_IMAGE : ", image_path)
        img = cv2.imread(image_path, 1)
        print("img : ", img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        processed_image_path = 'processed_image.png'
        cv2.imwrite(processed_image_path, thresh_img)
        print("processed_image_path : ", processed_image_path)
        return processed_image_path
    """

    def process_quotations(self):
        """ Méthode qui récupère les informations de chaque devis """
        print("EXECUTION METHODE process_quotations()")
        for image_path in self.image_paths:
            text = self.extract_text(image_path)
            self.extracted_texts.append(text)



    def extract_text(self, image_path):
        """ Méthode qui utilise Tesseract pour extraire le texte """
        print("EXECUTION METHODE extract_text()")
        try:
            print("image_path : ", image_path)
            processed_image_path = self.preprocess_image(image_path)
            image = Image.open(processed_image_path)
            extracted_text = pytesseract.image_to_string(image, lang='fra', config='--psm 6 --oem 3')
            print("extracted_text par pytesseract : ", extracted_text)
            return extracted_text
        except pytesseract.TesseractError as e:
            print(f"Une erreur Tesseract s'est produite : {e}")
        except Exception as e:
            print(f"Une erreur est survenue lors du traitement de {image_path} : {e}")
        return ""








    """ ***************** Méthodes en charge de l'enregistrement des données des devis en BDD ***************** """

    def store_texts_in_vector_db(self, text):
        """ Méthode qui stocke les données des devis sous forme non structurée dans la BDD Vectorielle """
        print("EXECUTION METHODE : store_texts_in_vector_db")
        print("TEXT : ", text)
        embedding = self.vector_db.generate_embedding(text)  # Utilise le modèle de VectorDataBase pour générer l'embedding
        metadata = {"Devis": f"Devis {len(self.processed_texts)}"}
        self.vector_db.insert(embedding, metadata=metadata)








    """ ***************** Méthodes en charge de la récupération et de l'affichage des données clés ***************** """

    def extract_relevant_info(self, text):
        """ Méthode qui extrait les infos clés de chaque devis """
        print("EXECUTION METHODE extract_relevant_info()")
        print("TEXT : ", text)
        devis_pattern = r"(?i)devis\s*(\d+|ref[\.:]?\s*\w+)"
        enterprise_pattern = r"(?i)(entreprise|émetteur|société)[\.:]?\s*(.+)"
        total_montant_pattern = r"(?i)montant[\s\w]*[\.:]?\s*(\d[\d\s,.€]*\d)"
        conditions_pattern = r"(?i)conditions[\s\w]*[\.:]?\s*(.+)"
        duree_validite_pattern = r"(?i)(validité|durée)[\s\w]*[\.:]?\s*(.+)"
        info = {
            "Devis": self.extract_value_using_pattern(text, devis_pattern),
            "Entreprise": self.extract_value_using_pattern(text, enterprise_pattern),
            "Montant": self.extract_value_using_pattern(text, total_montant_pattern),
            "Conditions": self.extract_value_using_pattern(text, conditions_pattern),
            "Validité": self.extract_value_using_pattern(text, duree_validite_pattern)
        }
        return info



    def extract_value_using_pattern(self, text, pattern):
        """ Méthode qui extrait des valeurs basées sur un pattern regex """
        print("EXECUTION METHODE extract_value_using_pattern()")
        print("TEXT : ", text)
        print("PATTERN : ", pattern)
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return "Non spécifié"



    def compare_quotations(self):
        """ Méthode qui compare les devis """
        print("EXECUTION METHODE compare_quotations()")
        self.process_quotations()
        for text in self.processed_texts:
            # Stocker le texte brut dans la BDD vectorielle :
            self.store_texts_in_vector_db(text)
            # Extraire les infos structurées pour affichage comparatif :
            info = self.extract_relevant_info(text)
            self.devis_data.append(info)
        self.display_comparison_table()



    def display_comparison_table(self):
        """ Affichage des devis dans un tableau comparatif """
        print("EXECUTION METHODE display_comparison_table()")
        headers = ["Devis", "Entreprise", "Montant", "Conditions", "Validité"]
        rows = []
        for data in self.devis_data:
            rows.append([data.get(header, "Non spécifié") for header in headers])
        # Afficher sous forme de tableau
        print(f"{' | '.join(headers)}")
        print("-" * (len(headers) * 20))
        for row in rows:
            print(f"{' | '.join(row)}")

