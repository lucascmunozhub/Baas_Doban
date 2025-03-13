from fastapi import FastAPI
from app.handshake import router as handshake_router
from app.callback import router as callback_router
from app.teste import router as teste_router 

app = FastAPI(title="Minha API de Integração")

# Incluindo as rotas
app.include_router(handshake_router, prefix="/handshake", tags=["Handshake"])
app.include_router(callback_router, prefix="/callback", tags=["Callback"])
app.include_router(teste_router, prefix="/teste", tags=["Teste"])

@app.get("/")
async def root():
    return {"message": "API de Integração rodando!"}
