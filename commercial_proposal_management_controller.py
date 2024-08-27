from fastapi import FastAPI
from services.QuotationManagementService import QuotationManagementService
from services.GenerateCommercialProposalService import GenerateCommercialProposalService








""" **************************************** Commande pour démarrer l'application **************************************** """

# uvicorn commercial_proposal_management_controller:app --reload --workers 1 --host 0.0.0.0 --port 8011








""" **************************************** Chargement de l'Api **************************************** """

app = FastAPI()








""" **************************************** Api de test **************************************** """

@app.get("/ping")
async def pong():
    return {"pong!"}








""" **************************** Manipulation du modèle LLM **************************** """

@app.get("/load-quotations")
async def load_quotations():
    """ Controller qui charge les devis et les informations de l'entreprise dans la BDD vectorielle """
    quotationManagementService = QuotationManagementService()
    return {quotationManagementService.execute_full_comparison()}



@app.get("/generate-commercial-proposal")
async def generate_commercial_proposal():
    """ Méthode qui génère la proposition commerciale en fonction des devis concurrents et des informations de l'entreprise """
    generateCommercialProposalService = GenerateCommercialProposalService()
    return {"message": generateCommercialProposalService.generate_commercial_proposal()}



@app.get("/test")
async def generate_commercial_proposal():
    """ Controller de test """
    generateCommercialProposalService = GenerateCommercialProposalService()
    return {"message": generateCommercialProposalService.test()}


