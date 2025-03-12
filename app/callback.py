from fastapi import APIRouter, Request, HTTPException
import logging
import asyncio
import json

router = APIRouter()

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

CALLBACK_STORAGE = []  # Simula um banco de dados em memória

@router.post("/")
async def receive_callback(request: Request):
    """
    Endpoint que recebe callbacks da BMP.
    """
    try:
        callback_data = await request.json()

        # Validação básica
        if "Header" not in callback_data or "Body" not in callback_data:
            raise HTTPException(status_code=400, detail="Formato inválido")

        # Armazena para processamento assíncrono
        CALLBACK_STORAGE.append(callback_data)

        logging.info(f"Callback recebido: {json.dumps(callback_data, indent=2, ensure_ascii=False)}")

        return {"status": "200 OK", "message": "Callback recebido com sucesso"}

    except Exception as e:
        logging.error(f"Erro ao processar callback: {str(e)}")
        raise HTTPException(status_code=400, detail="Erro no processamento do callback")

async def process_callbacks():
    while True:
        if CALLBACK_STORAGE:
            callback = CALLBACK_STORAGE.pop(0)
            logging.info(f"Processando callback: {callback}")
            await asyncio.sleep(2)  # Simula processamento
            logging.info(f"Callback {callback['Body']['IDTransacao']} processado!")
        await asyncio.sleep(1)

@router.on_event("startup")
async def startup_event():
    asyncio.create_task(process_callbacks())
