import uuid

from core import limpar_sessao, responder

COMANDOS = "Comandos: /limpar (zera o contexto em memória) | /sair (encerra a conversa)"


def main() -> None:
    session_id = str(uuid.uuid4())
    print("Chat com o Agente de IA - Quiz 3 IA Aplicada")
    print(COMANDOS)
    print()

    while True:
        try:
            entrada = input("Usuário: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break

        if not entrada:
            continue

        comando = entrada.lower()
        if comando == "/sair":
            print("Até logo!")
            break
        if comando == "/limpar":
            limpar_sessao(session_id)
            print("Contexto da conversa zerado.\n")
            continue
        if comando.startswith("/"):
            print(f"Comando desconhecido. {COMANDOS}\n")
            continue

        try:
            resposta = responder(entrada, session_id)
        except RuntimeError as erro:
            print(f"Erro de configuração: {erro}")
            break
        except Exception as erro:
            print(f"Erro ao consultar o modelo: {erro}\n")
            continue

        print(f"Agente: {resposta}\n")


if __name__ == "__main__":
    main()
