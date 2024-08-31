from fastapi import FastAPI
from services.QuotationProcessingService import QuotationProcessingService
from services.GenerateCommercialProposalService import GenerateCommercialProposalService






""" **************************************** Commande pour démarrer l'application **************************************** """

# uvicorn commercial_proposal_management_controller:app --reload --workers 1 --host 0.0.0.0 --port 8011






""" **************************************** Chargement de l'Api **************************************** """

app = FastAPI()






""" **************************************** Api de test **************************************** """

@app.get("/ping")
async def pong():
    return {"pong!"}






""" **************************** Endpoints des Fonctionnalités **************************** """

@app.get("/load-quotations")
async def load_quotations():
    """ Fonctionnalité qui charge les devis et les données de notre entreprise en BDD """
    quotationManagementService = QuotationProcessingService()
    return {quotationManagementService.load_quotations()}



@app.get("/generate-commercial-proposal")
async def generate_commercial_proposal():
    """ Fonctionnalité qui génère la proposition commerciale en fonction des devis concurrents et des informations de l'entreprise """
    generateCommercialProposalService = GenerateCommercialProposalService()
    return {"message": generateCommercialProposalService.generate_commercial_proposal()}

