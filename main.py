from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core import limpar_sessao, responder

app = FastAPI(title="Agente de IA", description="API de teste do chat - Quiz 3.")


class Pergunta(BaseModel):
    pergunta: str
    session_id: str = "default"


class Resposta(BaseModel):
    resposta: str
    session_id: str


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
