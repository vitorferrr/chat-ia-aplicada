# Agente de IA - Quiz 3 IA Aplicada

Chatbot inteligente com gerenciamento de memória conversacional, construído com LangChain e a API do Google Gemini. O projeto oferece tanto uma interface interativa via linha de comando (CLI) quanto uma API RESTful usando FastAPI. Link do chatbot:
- https://chat-ia-aplicada-w5ex.vercel.app/

---

## Arquitetura do Agente

```text
       +---------------------------------------------+
       |             Interface do Usuário            |
       |     (cli.py [Terminal] / main.py [FastAPI]) |
       +----------------------+----------------------+
                              | (Pergunta + session_id)
                              v
       +---------------------------------------------+
       |               Núcleo (core.py)              |
       |  +---------------------------------------+  |
       |  | ChatPromptTemplate (Sistema + Usuário)|  |
       |  +-------------------+-------------------+  |
       |                      |                      |
       |  +-------------------v-------------------+  |
       |  |  RunnableWithMessageHistory           |  |
       |  |  (InMemoryChatMessageHistory)         |  |
       |  +-------------------+-------------------+  |
       +----------------------|----------------------+
                              |
                              v
                 +--------------------------+
                 | ChatGoogleGenerativeAI   |
                 |   (gemini-2.5-flash)     |
                 +--------------------------+
```

---

## Como Funciona a Memória e o Contexto

O agente utiliza o mecanismo `RunnableWithMessageHistory` associado ao `InMemoryChatMessageHistory` do LangChain. 
- Cada interação é atrelada a uma chave identificadora (`session_id`), gerada via UUID no terminal ou repassada pelo corpo da requisição na API.
- As mensagens anteriores são armazenadas em memória (dicionário `_historicos`) e injetadas dinamicamente no prompt.
- É possível limpar o contexto de uma sessão específica usando o comando `/limpar` (no CLI) ou a rota `DELETE /sessao/{session_id}` (na API).

---

## Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior.
- Chave de API do Google Gemini (Google AI Studio).

### 1. Instalação e Configuração
Clone o repositório, crie um ambiente virtual e instale as dependências:

```bash
# Criação do ambiente virtual
python -m venv venv

# Ativação (Windows)
.\venv\Scripts\activate
# Ativação (Linux/macOS)
source venv/bin/activate

# Instalação das bibliotecas
pip install -r requirements.txt
```

Configure suas variáveis de ambiente:
```bash
cp .env.example .env
```
Abra o arquivo `.env` e insira sua `GOOGLE_API_KEY`.

---

### 2. Execução via Terminal (CLI)
Para uma interação direta no terminal com geração automática de `session_id`:
```bash
python cli.py
```
- Digite sua pergunta normalmente.
- Use `/limpar` para zerar a memória da conversa atual.
- Use `/sair` para encerrar o programa.

---

### 3. Execução via API (FastAPI)
Para subir o servidor web e testar as rotas:
```bash
uvicorn main:app --reload
```
Acesse a documentação interativa (Swagger) em: **http://localhost:8000/docs**

**Rotas Disponíveis:**
- `POST /chat`: Envia uma pergunta e o `session_id`.
- `DELETE /sessao/{session_id}`: Limpa o histórico em memória daquela sessão.

---

## Integrantes do grupo:
- Andressa Karine
- Beatriz Farias
- Marconi Andrade
- Vitor Ferreira
