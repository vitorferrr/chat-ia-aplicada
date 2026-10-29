import os

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODELO = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = (
    "Você é um assistente prestativo e objetivo. "
    "Responda sempre em português do Brasil, de forma clara e concisa. "
    "Use o histórico da conversa para manter o contexto das respostas."
)

_historicos: dict[str, InMemoryChatMessageHistory] = {}


def _obter_historico(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _historicos:
        _historicos[session_id] = InMemoryChatMessageHistory()
    return _historicos[session_id]


def _criar_chain() -> RunnableWithMessageHistory:
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY não encontrada. Copie .env.example para .env e preencha a chave."
        )

    llm = ChatGoogleGenerativeAI(model=MODELO, temperature=0.7)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("historico"),
            ("human", "{pergunta}"),
        ]
    )
    return RunnableWithMessageHistory(
        prompt | llm | StrOutputParser(),
        _obter_historico,
        input_messages_key="pergunta",
        history_messages_key="historico",
    )


_chain: RunnableWithMessageHistory | None = None


def responder(pergunta: str, session_id: str = "default") -> str:
    global _chain
    if _chain is None:
        _chain = _criar_chain()
    return _chain.invoke(
        {"pergunta": pergunta},
        config={"configurable": {"session_id": session_id}},
    )


def limpar_sessao(session_id: str = "default") -> None:
    _historicos.pop(session_id, None)


if __name__ == "__main__":
    print(responder("Meu nome é Vitor. Qual é a capital da França?", "teste"))
    print(responder("Qual é o meu nome?", "teste"))
