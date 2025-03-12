from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import json
import os

router = APIRouter()

# Carrega a chave HMAC da variável de ambiente (ou usa uma padrão para desenvolvimento)
HMAC_SECRET_KEY = os.getenv("HMAC_SECRET_KEY", "sua_chave_hmac_secreta")

def verify_hmac_signature(body: dict, received_signature: str) -> bool:
    """
    Verifica a assinatura HMAC da requisição recebida.
    """
    body_str = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
    calculated_signature = hmac.new(
        HMAC_SECRET_KEY.encode(), body_str.encode(), hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(calculated_signature, received_signature)

@router.post("/")
async def handshake(request: Request):
    """
    Endpoint de Handshake para validar transações recebidas.
    """
    try:
        headers = request.headers
        body = await request.json()

        # Obtém a assinatura HMAC enviada
        received_signature = headers.get("X-HMAC-Signature")
        if not received_signature:
            raise HTTPException(status_code=400, detail="HMAC signature missing")

        # Verifica a assinatura HMAC
        if not verify_hmac_signature(body, received_signature):
            raise HTTPException(status_code=403, detail="Invalid HMAC signature")

        return {"status": "200 OK", "message": "Handshake validado"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
