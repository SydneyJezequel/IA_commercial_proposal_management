import pytesseract
from PIL import Image
import cv2
from ..BO.Llm import Llm






class QuotationsComparator:
    """ Classe qui traite les devis """



    def __init__(self, image_paths):
        """ Constructeur """
        self.image_paths = image_paths
        self.processed_texts = []
        self.devis_data = []


    def preprocess_image(self, image_path):
        """ Méthode qui pré-traite l'image """
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        processed_image_path = 'processed_image.png'
        cv2.imwrite(processed_image_path, thresh_img)
        return processed_image_path



    def extract_text(self, image_path):
        """ Méthode qui utilise Tesseract pour extraire le texte """
        try:
            processed_image_path = self.preprocess_image(image_path)
            image = Image.open(processed_image_path)
            extracted_text = pytesseract.image_to_string(image, lang='fra', config='--psm 6 --oem 3')
            return extracted_text
        except pytesseract.TesseractError as e:
            print(f"Une erreur Tesseract s'est produite : {e}")
        except Exception as e:
            print(f"Une erreur est survenue lors du traitement de {image_path} : {e}")
        return ""



    def process_quotations(self):
        """ Méthode qui traite chaque devis et extrait le texte """
        for image_path in self.image_paths:
            text = self.extract_text(image_path)
            self.processed_texts.append(text)
    


    def analyze_texts(self, llm, question):
        """ Méthode qui analyse le texte extrait avec le LLM """
        results = []
        for text in self.processed_texts:
            prompt = f"{question} Répondez uniquement avec les informations clés en une seule ligne.\nTexte extrait:\n{text}"
            answer = llm.generate_answer(prompt)
            results.append(answer.strip())
        return results



    def compare_quotations(self, question="Affiche un tableau qui liste pour chaque devis, l'entreprise émétrice, le montant total du devis, les conditions de paiements, la durée de validité du devis."):
        """ Méthode qui compare les résultats des devis """
        self.process_quotations()
        llm = Llm()
        analysis_results = self.analyze_texts(llm, question)
        for i, result in enumerate(analysis_results):
            print(f"Devis {i+1} :\n{result}\n")

