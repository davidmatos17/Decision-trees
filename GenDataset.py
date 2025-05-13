import sys
import os
import csv
import random
from copy import deepcopy


game_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Game'))
sys.path.append(game_path)

from Game.searchAlgos.mcts import MCTS
from Game.fourGame import FourGame  

def gerar_dataset_csv(num_amostras=20000, path='datasets/connect4_dataset.csv', simbolo_ia='X'):
    with open(path, mode='w', newline='') as f:
        writer = csv.writer(f)

        header = [f"cell_{row}_{col}" for row in range(6) for col in range(7)]
        header.append("piece_count")
        header.append("best_move")
        writer.writerow(header)

        exemplos_gerados = 0
        tentativas = 0

        while exemplos_gerados < num_amostras and tentativas < num_amostras * 10:
            tentativas += 1
            print(f"\n Tentativa #{tentativas}")

            game = FourGame(columns=7, lines=6)
            jogadas_totais = random.randint(6, 41)  # mid to late-game

            # Varia o foco posicional: esquerda, centro ou direita
            pos_focus = random.choice(["left", "center", "right","random"])

            jogador = 'O' if simbolo_ia == 'X' else 'X'

            for i in range(jogadas_totais - 1):
                legal = game.getLegalMoves()
                if not legal or game.gameOver():
                    break

                # Filtra jogadas com base no foco posicional
                if pos_focus == "left":
                    legal_focus = [col for col in legal if col <= 2]
                elif pos_focus == "center":
                    legal_focus = [col for col in legal if 2 <= col <= 4]
                elif pos_focus == "right":
                    legal_focus = [col for col in legal if col >= 4]
                else:
                    legal_focus = [col for col in legal if col <=6]

                if not legal_focus:
                    legal_focus = legal  # fallback

                move = random.choice(legal_focus)
                game.makeMove(move + 1, jogador)
                jogador = 'O' if jogador == 'X' else 'X'

            if game.gameOver():
                print(" Jogo terminou antes do MCTS.")
                continue

            mcts = MCTS(iaSymbol=simbolo_ia, game=deepcopy(game))
            mcts.search(0.5)
            best = mcts.bestMove()
            if not best:
                print("MCTS falhou.")
                continue

            best_move = best.move
            game.makeMove(best_move + 1, simbolo_ia)

            # Cria entrada no CSV
            estado = []
            piece_count = 0
            for row in game.state:
                for cell in row:
                    if cell == 'X':
                        estado.append(1)
                        piece_count += 1
                    elif cell == 'O':
                        estado.append(2)
                        piece_count += 1
                    else:
                        estado.append(0)

            writer.writerow(estado + [piece_count, best_move])
            exemplos_gerados += 1
            print(f"Exemplo #{exemplos_gerados} gerado. Foco: {pos_focus}")

    print(f"\n{exemplos_gerados} exemplos gerados com sucesso em {path}")

if __name__ == "__main__":
    gerar_dataset_csv(num_amostras=20000)
