OBJECTIF DE CE PROJET :

Cette fonctionnalité utilise de l'IA pour :
1- Comparer des offres commercial en fonction d'un besoin.
2- Rédiger un argumentaire commercial pour positionner l'une des offres par rapport aux autres.

Remarques : Ce projet utilise un LLM via une Api. Dans un contexte professionnel, un LLM maison doit être utilisé pour assurer la confidentialité de vos données.




TUTORIEL :

1- Démarrer l'application avec la commande suivante :
uvicorn commercial_proposal_management_controller:app --reload --workers 1 --host 0.0.0.0 --port 8011

2- Charger les données contenues dans les devis en renseignant cette url :
http://localhost:8011/load-quotations
Puis suivez les logs d'exécution de cette fonctionnalité dans votre IDE.

3- Générer une offre commercial prenant en compte les devis existants et les données de l'entreprise via le endpoint suivant :
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


