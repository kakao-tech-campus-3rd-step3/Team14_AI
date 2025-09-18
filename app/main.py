from fastapi import FastAPI
from .routers.festivals import router as festivals_router
from .routers.preferences import router as ai_router

app = FastAPI(title="Festapick API", version="1.1.0")

@app.get("/test")
def test():
    return {"status": "ok"}

app.include_router(festivals_router)
app.include_router(ai_router)
