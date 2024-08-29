OBJECTIF DE CE PROJET :
Cette fonctionnalité utilise de l'IA pour :
1- Comparer des offres commercial en fonction d'un besoin.
2- Rédiger un argumentaire commercial pour positionner l'une des offres par rapport aux autres.




REMARQUES PREALABLES :
* Ce projet utilise un LLM via une Api. Dans un contexte professionnel, un LLM propre à l'entreprise doit être utilisé pour assurer la confidentialité de vos données.
* Le dataset utilisé est composé de devis tous basés sur le même format. Dans un contexte professionnel, il faut améliorer les traitements pour gérer d'autres formats de devis avec des résolutions parfois plus faible.
* En ajustant ce code, il doit pouvoir être utilisable pour différents types d'offres (ex : offre de produits bancaires).




TUTORIEL :

1- Renseigner les champs suivants de votre devis dans le fichier CONFIG.py
Exemple :
NUMERO_DEVIS = "001"
SOCIETE = "Plomberie Brestoise du 29"
ADRESSE_SOCIETE = "123 Rue de Verdun 29200 Brest"
DATE_DEVIS = "2024-08-29"
DEBUT_TRAVAUX = "2024-09-01"

2- Démarrer l'application avec la commande suivante :
uvicorn commercial_proposal_management_controller:app --reload --workers 1 --host 0.0.0.0 --port 8011

3- Charger les données contenues dans les devis en renseignant cette url :
http://localhost:8011/load-quotations
Puis suivez les logs d'exécution de cette fonctionnalité dans votre IDE.

4- Générer une offre commercial prenant en compte les devis existants et les données de l'entreprise via le endpoint suivant :
http://localhost:8011//generate-commercial-proposal
Puis suivez les logs d'exécution de cette fonctionnalité dans votre IDE.




MODELES UTILISEES :
* Le modèle utilisé pour récupéré pour récupérer les informations textuelles dans les devis est modèle un OCR (Optical Character Recognition).
* Le LLM utilisé est LLAMA3 via MONSTER API : 
https://monsterapi.ai/user/playground?model=meta-llama/Meta-Llama-3-8B-Instruct




DEPENDANCES UTILISEES :




COMMANDES PERSO :

export PYTHONPATH=/Users/sjezequel/PycharmProjects/CommercialProposals:$PYTHONPATH
echo $PYTHONPATH

