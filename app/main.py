from teste import ItemPayload
from fastapi import FastAPI, Request, HTTPException
from teste import ItemPayload
import hmac
import hashlib
import base64
import os

app = FastAPI()


# Chave secreta HMAC (em um ambiente real, armazene isso em uma variável de ambiente segura)
HMAC_SECRET = os.getenv("HMAC_SECRET", "sua_chave_super_secreta")

def verify_hmac_signature(data: str, received_signature: str) -> bool:
    """Valida a assinatura HMAC da requisição"""
    computed_hmac = hmac.new(HMAC_SECRET.encode(), data.encode(), hashlib.sha256).digest()
    computed_signature = base64.b64encode(computed_hmac).decode()
    return hmac.compare_digest(computed_signature, received_signature)

@app.post("/handshake")
async def handshake(request: Request):
    body = await request.body()
    received_signature = request.headers.get("X-HMAC-Signature")
    
    expected_signature = base64.b64encode(hmac.new(HMAC_SECRET.encode(), body, hashlib.sha256).digest()).decode()
    
    print(f"Esperado: {expected_signature}")
    print(f"Recebido: {received_signature}")

    if not received_signature or not hmac.compare_digest(expected_signature, received_signature):
        raise HTTPException(status_code=401, detail="Assinatura HMAC inválida")

    return {"status": "OK"}
