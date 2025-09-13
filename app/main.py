from fastapi import FastAPI
from .routers.festivals import router as festivals_router

app = FastAPI(title="Festapick API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(festivals_router)
