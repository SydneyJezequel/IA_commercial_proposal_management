import json
import math
import re
import config
from BO.Llm import Llm
from BO.SqlDatabase import SqlDatabase
from services.GetQuotationsDataService import GetQuotationsDataService






class QuotationManagementService:
    """ Classe chargée du traitement et de la comparaison des devis """




    """ ***************** Constructeur ***************** """

    def __init__(self, db_url=config.DB_URL):
        """ Constructeur """
        # Service qui récupère le texte des devis :
        self.get_quotations_data_service = GetQuotationsDataService()
        # Initialisation de la BDD SQLlite :
        self.sql_service = SqlDatabase()




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
        """ Méthode pour parser et valider la réponse du LLM. """
        # Parsing de la réponse et normalisation
        normalized_info = {
            'devis': response.get('Numéro de devis', 'Non spécifié'),
            'entreprise': response.get('Société', 'Non spécifié'),
            'adresse_entreprise': response.get('Adresse de la société', 'Non spécifié'),
            'date': response.get('Date du devis', 'Non spécifié'),
            'client': response.get('Nom du client', 'Non spécifié'),
            'adresse_client': response.get('Adresse du client', 'Non spécifié'),
            'code_postal_client': response.get('Code Postal du client', 'Non spécifié'),
            'description': response.get('Description du travail', 'Non spécifié'),
            'montant_total': float(self.normalize_and_convert_amount(response.get('Montant total HT', '0 EUR').replace(' EUR', ''))),
            'taux_tva': float(self.normalize_and_convert_amount(response.get('Taux de TVA', '0%').replace('%', ''))),
            'total_ttc': float(self.normalize_and_convert_amount(response.get('Montant total TTC', '0 EUR').replace(' EUR', ''))),
            'conditions': response.get('Conditions de règlement', 'Non spécifié'),
            'debut_travaux': response.get('Début des travaux', 'Non spécifié')
        }
        print("INFO RECUPEREE : ", normalized_info)
        # Validation et correction des données extraites
        normalized_info = self.validate_and_correct_info(normalized_info)
        return normalized_info



    def normalize_and_convert_amount(self, amount_str):
        """ Méthode qui supprime les séparateurs de milliers et remplace les virgules par des points. """
        try:
            # Suppression des espaces et changement des , par des points :
            normalized_amount = amount_str.replace(' ', '').replace(',', '.')
            return float(normalized_amount)
        except ValueError as e:
            print(f"Erreur de conversion : {e} avec la chaîne '{amount_str}'")
            return 0.0  # Return a default value or handle appropriately



    def validate_and_correct_info(self, info):
        """ Méthode pour valider et corriger les informations extraites. """
        # Validation du montant total, du taux de TVA et du montant TTC
        if (info['montant_total'] != 0.0) and (info['taux_tva'] != 0.0) and (info['total_ttc'] != 0.0):
            try:
                montant_ht = info['montant_total']  # Directement depuis normalized_info
                taux_tva = info['taux_tva'] / 100  # Normalisé
                total_ttc_calculated = montant_ht * (1 + taux_tva)
                total_ttc_extracted = info['total_ttc']  # Normalisé
                if not math.isclose(total_ttc_calculated, total_ttc_extracted, rel_tol=1e-2):
                    info['total_ttc'] = f"{total_ttc_calculated:.2f} EUR"  # Correction du montant TTC si nécessaire
            except ValueError:
                print("Erreur de conversion lors de la validation des montants.")
        return info
    


    def load_quotations(self):
        """ Méthode pour comparer les devis """
        # Récupération du contenu brut dans les devis :
        self.get_quotations_data_service.process_quotations()
        print("ETAPE 1 : CHARGEMENT DES DEVIS BRUTS : ", self.get_quotations_data_service.extracted_texts)
        # Traitement de chaque devis :
        print("ETAPE 2 : NETTOYAGE DES DEVIS & INTEGRATION EN BDD : ")
        for i, text in enumerate(self.get_quotations_data_service.extracted_texts):
            # ==> *********************************** TEST ***********************************
            print("TOUR DE BOUCLE : ", i)
            # ==> *********************************** TEST ***********************************
            # Extraction des informations structurées :
            info = self.extract_relevant_info(text)
            print("DEVIS N° {i} RECUPERE : ", info)
            # Enregistrement des Devis en BDD :
            devis_instance = self.sql_service.save_devis(info)
            print("DEVIS INTEGRE EN BDD : ", devis_instance)
            # ==> *********************************** LE PB A LIEU AVANT L'ETAPE 3 ***********************************
        print("AFFICHAGE DES DEVIS DE LA BDD SQLITE : ", self.sql_service.get_all_devis())
        print("ETAPE 3 : AFFICHAGE DES DEVIS ET RENVOI DES DEVIS DANS UN FICHIER JSON : ")
        self.display_comparison_table()



    def display_comparison_table(self):
        """ Retrieve and return the quotations in a comparative list """
        print("EXECUTING METHOD display_comparison_table()")

        # Récupérer tous les devis depuis la base de données
        all_devis = self.sql_service.get_all_devis()

        # Création de l'array :
        headers = ["Devis", "Entreprise", "Montant", "Conditions", "Validité"]
        
        # Correspondance entre les headers et les attributs des objets devis
        attribute_mapping = {
            "Devis": "devis",
            "Entreprise": "entreprise",
            "Montant": "montant_total",
            "Conditions": "conditions",
            "Validité": "date"  # Remplacer par l'attribut approprié si besoin
        }
        
        devis_list = []
        for devis in all_devis:
            devis_dict = {
                header: getattr(devis, attribute_mapping[header], "Non spécifié")
                for header in headers
            }
            devis_list.append(devis_dict)
        
        print("DEVIS LIST RENVOYEE : ", devis_list)
        # Optionnel : affichage de la liste dans la console pour vérification
        print(f"{' | '.join(headers)}")
        print("-" * (len(headers) * 20))
        for devis in devis_list:
            print(f"{' | '.join(map(str, devis.values()))}")
        
        return devis_list

















































































































































    """
    def extract_value_using_pattern(self, text, pattern):
        # Méthode qui extrait des valeurs basées sur un pattern regex
        print("EXECUTION METHODE extract_value_using_pattern()")
        print("TEXT : ", text)
        print("PATTERN : ", pattern)
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return "Non spécifié"
    """


