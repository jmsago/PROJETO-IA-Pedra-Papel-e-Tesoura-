import random
import os

ACTIONS = ["pedra", "papel", "tesoura"]

# Q-Learning
Q = {}   # dicionário: (estado) -> valores para cada ação
alpha = 0.5       # taxa de aprendizado
gamma = 0.8       # desconto futuro
epsilon = 0.2     # probabilidade de explorar (jogada aleatória)

def q_get(state):
    if state not in Q:
        Q[state] = [0, 0, 0]  # valores para pedra, papel, tesoura
    return Q[state]

def escolher_acao(state):
    if random.random() < epsilon:
        return random.randint(0, 2)  # ação aleatória
    return max(range(3), key=lambda a: q_get(state)[a])

def resultado(jogador, ia):
    if jogador == ia:
        return 0  # empate
    if (jogador == 0 and ia == 2) or \
       (jogador == 1 and ia == 0) or \
       (jogador == 2 and ia == 1):
        return 1  # jogador venceu
    return -1     # IA venceu

def treinar_Q(old_state, action, reward, new_state):
    old_q = q_get(old_state)[action]
    future_q = max(q_get(new_state))
    new_q = old_q + alpha * (reward + gamma * future_q - old_q)
    Q[old_state][action] = new_q

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    last_player = "inicio"
    last_ia = "inicio"
    print("IA Pedra-Papel-Tesoura com Q-Learning")
    print("Jogue contra a IA e ela vai aprendendo!")
    print("Comandos: pedra, papel, tesoura ou sair")

    while True:
        jogador = input("\nSua jogada: ").lower().strip()

        if jogador == "sair":
            print("\nEncerrando…")
            break

        if jogador not in ACTIONS:
            print("Entrada inválida. Tente novamente.")
            continue

        player_idx = ACTIONS.index(jogador)

        # estado atual baseado na jogada anterior do jogador
        state = last_player

        # IA escolhe ação
        ia_idx = escolher_acao(state)
        ia = ACTIONS[ia_idx]

        print(f"IA jogou: {ia}")

        # resultado
        r = resultado(player_idx, ia_idx)

        if r == 1:
            print("Você venceu!")
        elif r == -1:
            print("A IA venceu!")
        else:
            print("Empate!")

        # treinar IA
        new_state = jogador
        treinar_Q(state, ia_idx, r, new_state)

        # atualizar histórico
        last_player = jogador
        last_ia = ia

if __name__ == "__main__":
    main()
