import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core import limpar_sessao, responder

load_dotenv()

ORIGENS_LOCAIS = ["http://localhost:3000", "http://localhost:5173"]
ORIGENS_PERMITIDAS = ORIGENS_LOCAIS + [
    o.strip().rstrip("/") for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()
]

app = FastAPI(title="Agente de IA", description="API de teste do chat - Quiz 3.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENS_PERMITIDAS,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pergunta(BaseModel):
    pergunta: str
    session_id: str = "default"


class Resposta(BaseModel):
    resposta: str
    session_id: str


@app.get("/")
def saude() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=Resposta)
def chat(corpo: Pergunta) -> Resposta:
    try:
        texto = responder(corpo.pergunta, corpo.session_id)
    except RuntimeError as erro:
        raise HTTPException(status_code=500, detail=str(erro))
    except Exception as erro:
        raise HTTPException(status_code=502, detail=f"Erro ao consultar o modelo: {erro}")
    return Resposta(resposta=texto, session_id=corpo.session_id)


@app.delete("/sessao/{session_id}")
def limpar(session_id: str) -> dict:
    limpar_sessao(session_id)
    return {"mensagem": f"Sessão '{session_id}' limpa."}
