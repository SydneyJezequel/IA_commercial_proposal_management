from fastapi import FastAPI
# from service.commercial_service_impl_V2







""" **************************************** Commande pour démarrer l'application **************************************** """

# uvicorn generate_commercial_proposal_controller:app --reload --workers 1 --host 0.0.0.0 --port 8011






""" **************************************** Chargement de l'Api **************************************** """

app = FastAPI()
# embedding_service = EmbeddingService()






""" **************************************** Api de test **************************************** """

@app.get("/ping")
async def pong():
    return {"pong!"}






""" **************************** Manipulation du modèle LLM **************************** """





