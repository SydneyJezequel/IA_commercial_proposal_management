from fastapi import FastAPI, HTTPException
from services.QuotationProcessingService import QuotationProcessingService
from services.GenerateCommercialProposalService import GenerateCommercialProposalService






""" **************************************** Commande pour démarrer l'application **************************************** """

# uvicorn commercial_proposal_controller:app --reload --workers 1 --host 0.0.0.0 --port 8011






""" **************************************** Chargement de l'Api **************************************** """

app = FastAPI()






""" **************************************** Api de test **************************************** """

@app.get("/ping")
async def pong():
    return {"pong!"}






""" **************************** Endpoints des Fonctionnalités **************************** """

@app.get("/load-quotations")
async def load_quotations():
    """ Fonctionnalité qui charge les devis et les données de notre entreprise en BDD. """

    try:
        quotation_management_service = QuotationProcessingService()
        result = quotation_management_service.load_quotations()
        return {"data": result}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")



@app.get("/generate-commercial-proposal")
async def generate_commercial_proposal():
    """ Fonctionnalité qui génère la proposition commerciale en fonction des devis concurrents et des informations de l'entreprise. """
    
    try:
        generate_commercial_proposal_service = GenerateCommercialProposalService()
        result = generate_commercial_proposal_service.generate_commercial_proposal()
        return {"message": result}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")
    
