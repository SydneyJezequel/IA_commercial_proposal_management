import re
import pytesseract
from PIL import Image
import cv2
from BO.VectorDatabase import VectorDataBase
from spellchecker import SpellChecker  # Utiliser le nom correct de la classe
import os
import config
from BO.Devis import Devis






class QuotationManagementService:
    """ Classe chargée du traitement et de la comparaison des devis """





    """ ***************** Constructeur ***************** """

    def __init__(self):
        """ Constructeur """
        # Emplacements des images :
        # self.image_paths = image_paths
        self.image_paths = [os.path.join(config.QUOTATIONS_FILES_PATH, image) for image in config.QUOTATIONS_FILES_LIST]
        print("Image paths initialized:", self.image_paths)
        # Contenu des devis :
        self.extracted_texts = []
        # Liste des informations sur les devis :
        self.devis_data = [] 
        # Bdd Vectorielle :
        self.vector_db = VectorDataBase()






    """ ***************** Méthode en charge du prétraitement et de l'extraction du texte des devis ***************** """


    def preprocess_image(self, image_path):
        """ Méthode qui pré-traite l'image et sauvegarde dans le répertoire de sortie """
        print("IMAGE_PATH IN PREPROCESS_IMAGE : ", image_path)
        # Lire l'image en niveaux de gris
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Appliquer l'égalisation d'histogramme
        img = cv2.equalizeHist(img)
        # Appliquer un filtre bilatéral pour réduire le bruit tout en gardant les contours nets
        img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        # Appliquer un seuillage adaptatif pour binariser l'image
        thresh_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                           cv2.THRESH_BINARY, 11, 2)
        # Déterminer le chemin de l'image traitée en changeant le répertoire
        processed_image_path = os.path.join(config.PROCESSED_QUOTATIONS_FILES_PATH, os.path.basename(image_path))
        # Sauvegarder l'image traitée
        cv2.imwrite(processed_image_path, thresh_img)
        print("processed_image_path : ", processed_image_path)
        return processed_image_path


    
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
            extracted_text = pytesseract.image_to_string(image, lang='fra', config='--psm 3 --oem 3')
            print("extracted_text par pytesseract : ", extracted_text)
            clean_text = self.clean_extracted_text(extracted_text)  # Correction de l'appel
            print("clean_extracted_text :", clean_text)
            return clean_text
        except pytesseract.TesseractError as e:
            print(f"Une erreur Tesseract s'est produite : {e}")
        except Exception as e:
            print(f"Une erreur est survenue lors du traitement de {image_path} : {e}")
        return ""



    def clean_extracted_text(self, text):
        """ Corrige le texte extrait """
        spell = SpellChecker(language='fr') 
        cleaned_text = []
        for word in text.split():
            corrected_word = spell.correction(word)
            cleaned_text.append(corrected_word if corrected_word else word)
        return ' '.join(cleaned_text)





    """ ***************** Méthodes en charge de l'enregistrement des données des devis en BDD ***************** """

    def store_texts_in_vector_db(self, text, devis_number):
        """ Méthode qui stocke les données des devis sous forme non structurée dans la BDD Vectorielle """
        print("EXECUTION METHODE : store_texts_in_vector_db")
        print("TEXT : ", text)
        embedding = self.vector_db.generate_embedding(text)  # Utilise le modèle de VectorDataBase pour générer l'embedding
        metadata = {"Devis": f"Devis {devis_number}"}
        self.vector_db.insert(embedding, metadata=metadata)








    """ ***************** Méthodes en charge de la récupération et de l'affichage des données clés ***************** """

    def extract_relevant_info(self, text):
        """ Méthode qui extrait les infos clés de chaque devis """
        # Regex pour extraire les informations :
        devis_pattern = r"Devis n°\s*:\s*(\d+)"
        enterprise_pattern = r"Société\s*:\s*(.+)"
        adresse_entreprise_pattern = r"Adresse\s*:\s*(.+)"
        date_pattern = r"Date\s*:\s*(\d{2}/\d{2}/\d{4})"
        client_pattern = r"Client\s*:\s*(.+)"
        adresse_client_pattern = r"Adresse\s*:\s*(.+)"
        code_postal_client_pattern = r"Code Postale\s*:\s*(\d+)"
        description_pattern = r"Pose d'une nouvelle chaudière"
        total_ht_pattern = r"TOTAL HT\s*(\d+,\d{2})\s*€"
        taux_tva_pattern = r"TAUX TVA\s*(\d+%)"
        total_ttc_pattern = r"TOTAL TTC\s*(\d+,\d{2})\s*€"
        debut_travaux_pattern = r"Début des travaux\s*:\s*(\d{2}/\d{2}/\d{4})"
        conditions_pattern = r"Conditions de règlement\s*:\s*(.+)"
        # Dictionnaire regroupant les données d'un devis :
        print("text : ", text)
        info = {
            "Devis": self.extract_value_using_pattern(text, devis_pattern),
            "Entreprise": self.extract_value_using_pattern(text, enterprise_pattern),
            "Adresse Entreprise": self.extract_value_using_pattern(text, adresse_entreprise_pattern),
            "Date": self.extract_value_using_pattern(text, date_pattern),
            "Client": self.extract_value_using_pattern(text, client_pattern),
            "Adresse Client": self.extract_value_using_pattern(text, adresse_client_pattern),
            "Code Postal Client": self.extract_value_using_pattern(text, code_postal_client_pattern),
            "Description": description_pattern,  # Assumé fixe dans cet exemple
            "Montant Total": self.extract_value_using_pattern(text, total_ht_pattern),
            "Taux TVA": self.extract_value_using_pattern(text, taux_tva_pattern),
            "Total TTC": self.extract_value_using_pattern(text, total_ttc_pattern),
            "Conditions": self.extract_value_using_pattern(text, conditions_pattern),
            "Début Travaux": self.extract_value_using_pattern(text, debut_travaux_pattern)
        }
        print("INFO : ", info)
        return info



    def map_data_to_devis(self, data):
        """ Méthode qui mappe les données extraites à une instance de la classe Devis """
        devis_instance = Devis(
            devis=data.get('Devis', 'Non spécifié'),
            entreprise=data.get('Entreprise', 'Non spécifié'),
            adresse_entreprise=data.get('Adresse Entreprise', 'Non spécifié'),
            date=data.get('Date', 'Non spécifié'),
            client=data.get('Client', 'Non spécifié'),
            adresse_client=data.get('Adresse Client', 'Non spécifié'),
            code_postal_client=data.get('Code Postal Client', 'Non spécifié'),
            description=data.get('Description', ''),
            montant_total=data.get('Montant Total', 'Non spécifié'),
            taux_tva=data.get('Taux TVA', 'Non spécifié'),
            total_ttc=data.get('Total TTC', 'Non spécifié'),
            conditions=data.get('Conditions', 'Non spécifié'),
            debut_travaux=data.get('Début Travaux', 'Non spécifié')
        )
        return devis_instance



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
        """ Method to compare quotations by converting them into instances of the Quotation class """
        print("EXECUTING METHOD compare_quotations()")
        self.process_quotations()

        for i, text in enumerate(self.extracted_texts):
            # Extract structured information
            info = self.extract_relevant_info(text)
            
            # Transform into a Quotation instance before storing in the vector database
            quotation_instance = self.map_data_to_devis(info)
            print("DEVIS INTEGRE EN BDD : ", quotation_instance)

            # Store the Quotation instance (or its text representation) in the vector database
            self.store_texts_in_vector_db(str(quotation_instance), i)
            print("STORAGE IN VECTOR DB COMPLETED")

            # Add the Quotation instance to self.devis_data
            self.devis_data.append(quotation_instance)
            print("RETRIEVING KEY QUOTATION INFORMATION: ", self.devis_data)
        
        self.display_comparison_table()



    def display_comparison_table(self):
        """ Display the quotations in a comparative table """
        print("EXECUTING METHOD display_comparison_table()")
        headers = ["Devis", "Entreprise", "Montant", "Conditions", "Validité"]
        
        rows = []
        for data in self.devis_data:
            rows.append([
                getattr(data, header.lower(), "Non spécifié")  # Access attributes dynamically
                for header in headers
            ])
        
        # Print the table
        print(f"{' | '.join(headers)}")
        print("-" * (len(headers) * 20))
        for row in rows:
            print(f"{' | '.join(row)}")



    def execute_full_comparison(self):
        """ Méthode encapsulant tout le processus de traitement et de comparaison des devis """
        print("Début de l'exécution complète")

        # Création des chemins des images
        images_to_process = config.QUOTATIONS_FILES_LIST
        images_to_process_paths = [os.path.join(config.QUOTATIONS_FILES_PATH, image) for image in images_to_process]
        print("Récupération des chemins : OK.")

        # Création de l'instance de la BDD Vectorielle
        vector_db_mock = VectorDataBase()
        print("Instanciation de la BDD : OK.")

        print("comparator.image_paths : ", self.image_paths)
        print("Instanciation de la classe QuotationsComparator + Vérification des chemins ==> OK")

        # Simulation du texte extrait pour chaque image
        extracted_texts = [self.extract_text(image_path) for image_path in images_to_process_paths]
        print("Extract_texts : ", extracted_texts)
        print("Extraction du texte dans chaque Image : OK.")

        # Affichage du tableau comparatif et stockage des devis en BDD Vectorielle
        self.compare_quotations()
        print("Stockage des données dans la BDD Vectorielle réalisé par cette méthode ==> OK")
        print("Récupération des infos clés des devis ==> OK.")

        print("********** FIN DES TESTS ************")




