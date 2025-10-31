from fastapi import FastAPI
#from .routers.festivals import router as festivals_router
from .routers.ai_features import router as ai_features
from .routers.ai_model_reco import router as ai_model_reco

app = FastAPI(title="Festapick API", version="1.1.0")

@app.get("/test")
def test():
    return {"status": "ok"}

#app.include_router(festivals_router)
app.include_router(ai_model_reco)
app.include_router(ai_features)
