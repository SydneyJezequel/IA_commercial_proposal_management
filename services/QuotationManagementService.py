import json
import math
import re
import pytesseract
from PIL import Image
import cv2
from BO.VectorDatabase import VectorDataBase
from spellchecker import SpellChecker  # Utiliser le nom correct de la classe
import os
import config
from BO.Devis import Devis
from BO.Llm import Llm






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
        """Méthode qui extrait les infos clés de chaque devis en utilisant un LLM avec prétraitement et validation."""
        # Étape 1 : Prétraitement du texte
        preprocessed_text = self.preprocess_text(text)
        
        # Étape 2 : Génération de la requête pour le LLM en demandant un JSON structuré
        llm_prompt = f"""
        Voici un texte de devis. Extrais les informations suivantes et renvoie les sous forme de JSON structuré :
        {{
            "Numéro de devis": "",
            "Société": "",
            "Adresse de la société": "",
            "Date du devis": "",
            "Nom du client": "",
            "Adresse du client": "",
            "Code Postal du client": "",
            "Description du travail": "",
            "Montant total HT": "",
            "Taux de TVA": "",
            "Montant total TTC": "",
            "Début des travaux": "",
            "Conditions de règlement": ""
        }}
        
        Texte :
        {preprocessed_text}
        """
        
        # Étape 3 : Interaction avec le LLM pour extraire les informations
        llm = Llm()
        response = llm.generate_answer(llm_prompt)
        print("RESPONSE OBTENUE DU LLM : ", response)
        
        # Étape 4 : Vérification si la réponse est un JSON valide
        response_dict = self.manual_parse_llm_response(response)
        print("REPONSE RECUPEREE AVEC manual_parse_llm_response() : ", response_dict)

        # Étape 5 : Parsing et validation des données extraites
        info = self.parse_and_validate_llm_response(response_dict)
        print("RESPONSE PARSÉE DU LLM : ", info)
        return info



    def manual_parse_llm_response(self, response_text):
        """Méthode pour extraire manuellement les données du texte brut en cas d'échec du parsing JSON."""
        # Étape 1 : Extraction de la partie JSON de la réponse
        json_start = response_text.find("{")
        json_end = response_text.rfind("}")
        if json_start != -1 and json_end != -1:
            # Extraire la chaîne JSON potentielle
            json_potential = response_text[json_start:json_end + 1]
            # Étape 2 : Tenter de parser cette chaîne comme JSON
            try:
                info = json.loads(json_potential)
                return info  # Si succès, retourner l'objet JSON parsé
            except json.JSONDecodeError:
                print("Erreur : La partie extraite ne peut pas être parsée en JSON.")
        # Si on arrive ici, cela signifie que le JSON n'a pas pu être extrait correctement
        print("Erreur : Impossible de trouver un JSON valide dans la réponse.")
        # Optionnel : Retourner un dictionnaire vide ou un message d'erreur structuré
        return {
            "Devis": "Non spécifié",
            "Entreprise": "Non spécifié",
            "Adresse Entreprise": "Non spécifié",
            "Date": "Non spécifié",
            "Client": "Non spécifié",
            "Adresse Client": "Non spécifié",
            "Code Postal Client": "Non spécifié",
            "Description": "Non spécifié",
            "Montant Total": "Non spécifié",
            "Taux TVA": "Non spécifié",
            "Total TTC": "Non spécifié",
            "Conditions": "Non spécifié",
            "Début Travaux": "Non spécifié"
        }




    def preprocess_text(self, text):
        """Méthode pour prétraiter le texte avant l'extraction."""
        # Remplacement des caractères spéciaux, uniformisation des montants, etc.
        text = text.replace("€", " EUR")  # Remplace le symbole € par EUR pour uniformiser
        text = re.sub(r'(\d+)[.,](\d{2})', r'\1.\2', text)  # Uniformise les montants 1.800,00 en 1800.00
        text = re.sub(r'\s+', ' ', text)  # Supprime les espaces multiples pour éviter les erreurs de lecture
        return text



    def parse_and_validate_llm_response(self, response):
        """Méthode pour parser et valider la réponse du LLM."""
        # Parsing de la réponse
        info = {
            "Devis": response.get('Numéro de devis', 'Non spécifié'),
            "Entreprise": response.get('Société', 'Non spécifié'),
            "Adresse Entreprise": response.get('Adresse de la société', 'Non spécifié'),
            "Date": response.get('Date du devis', 'Non spécifié'),
            "Client": response.get('Nom du client', 'Non spécifié'),
            "Adresse Client": response.get('Adresse du client', 'Non spécifié'),
            "Code Postal Client": response.get('Code Postal du client', 'Non spécifié'),
            "Description": response.get('Description du travail', 'Non spécifié'),
            "Montant Total": response.get('Montant total HT', 'Non spécifié'),
            "Taux TVA": response.get('Taux de TVA', 'Non spécifié'),
            "Total TTC": response.get('Montant total TTC', 'Non spécifié'),
            "Conditions": response.get('Conditions de règlement', 'Non spécifié'),
            "Début Travaux": response.get('Début des travaux', 'Non spécifié')
        }
        # Validation et correction des données extraites
        info = self.validate_and_correct_info(info)
        return info



    def validate_and_correct_info(self, info):
        """Méthode pour valider et corriger les informations extraites."""
        # Validation du montant total, du taux de TVA et du montant TTC
        if info['Montant Total'] != 'Non spécifié' and info['Taux TVA'] != 'Non spécifié' and info['Total TTC'] != 'Non spécifié':
            try:
                montant_ht = float(info['Montant Total'].replace(',', '.').replace(' EUR', ''))
                taux_tva = float(info['Taux TVA'].replace('%', '')) / 100
                total_ttc_calculated = montant_ht * (1 + taux_tva)
                total_ttc_extracted = float(info['Total TTC'].replace(',', '.').replace(' EUR', ''))
                if not math.isclose(total_ttc_calculated, total_ttc_extracted, rel_tol=1e-2):
                    info['Total TTC'] = f"{total_ttc_calculated:.2f} EUR"  # Correction du montant TTC si nécessaire
            except ValueError:
                print("Erreur de conversion lors de la validation des montants.")
        # Autres validations spécifiques peuvent être ajoutées ici
        return info



    def map_data_to_devis(self, data):
        """ Méthode qui mappe les données extraites à une instance de la classe Devis """
        print("DEVIS CHARGE DANS LA METHODE map_data_to_devis : ", data)
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
        print("VALEUR AFFECTEES AU DEVIS : ")
        print(f"Devis: {data.get('Devis', 'Non spécifié')}")
        print(f"Entreprise: {data.get('Entreprise', 'Non spécifié')}")
        print(f"Adresse Entreprise: {data.get('Adresse Entreprise', 'Non spécifié')}")
        print(f"Date: {data.get('Date', 'Non spécifié')}")
        print(f"Client: {data.get('Client', 'Non spécifié')}")
        print(f"Adresse Client: {data.get('Adresse Client', 'Non spécifié')}")
        print(f"Code Postal Client: {data.get('Code Postal Client', 'Non spécifié')}")
        print(f"Description: {data.get('Description', '')}")
        print(f"Montant Total: {data.get('Montant Total', 'Non spécifié')}")
        print(f"Taux TVA: {data.get('Taux TVA', 'Non spécifié')}")
        print(f"Total TTC: {data.get('Total TTC', 'Non spécifié')}")
        print(f"Conditions: {data.get('Conditions', 'Non spécifié')}")
        print(f"Début Travaux: {data.get('Début Travaux', 'Non spécifié')}")
        print("DEVIS INSTANCE GENEREE : ", devis_instance)
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
            print("DEVIS RECUPERE : ", info)
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




