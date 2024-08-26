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
    quotationManagementService = QuotationManagementService()
    return {quotationManagementService.execute_full_comparison()}



@app.get("/generate-commercial-proposal")
async def generate_commercial_proposa():
    generateCommercialProposalService = GenerateCommercialProposalService()
    return {"message": generateCommercialProposalService.generate_commercial_proposal()}


