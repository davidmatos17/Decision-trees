from fourGame import FourGame

def showResults(game, result, winner):
    print(game)  # Mostrar o tabuleiro atual

    match result:
        case -1:
            print("Invalid Move! Please choose another column.")
            return False, True
        case 0:
            print("Nice Move!")
            return False, False
        case 1:
            print("It's a Draw!!")
            return True, False
        case 2:
            print(f"The symbol {winner} just won!")
            return True, False

def main():
    game = FourGame(7, 6)
    end = False

    move = input('Escolhe o símbolo com que queres jogar (X ou O): ').upper()

    if move not in ['X', 'O']:
        print('O símbolo deve ser X ou O')
        return

    player1 = move
    player2 = 'O' if player1 == 'X' else 'X'
    current_player = player1

    while not end:
        print(f"Player '{current_player}' turn")
        
        while True:
            try:
                col = int(input('Column (1-7): '))
                if col < 1 or col > 7:
                    raise ValueError
                break
            except ValueError:
                print("Invalid Input! Please enter a number from 1 to 7.")

        result, winner = game.makeMove(col, current_player)
        end, invalid = showResults(game, result, winner)

        # Se o movimento for inválido, o jogador repete
        if invalid:
            continue

        # Trocar jogador se o jogo ainda não acabou
        if not end:
            current_player = player2 if current_player == player1 else player1

    print("Game Over! Thanks for playing.")
    print("Final Results:")
    print(game)

if __name__ == '__main__':
    main()
