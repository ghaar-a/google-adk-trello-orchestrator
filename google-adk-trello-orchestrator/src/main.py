from agent import agent

def main():
    print("🤖 Agente Trello iniciado (digite 'sair' para encerrar)\n")

    while True:
        user_input = input("Você: ")

        if user_input.lower() == "sair":
            break

        resposta = agent(user_input)
        print(f"Agente: {resposta}\n")


if __name__ == "__main__":
    main()