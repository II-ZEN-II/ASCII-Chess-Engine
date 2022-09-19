import board

def main():
    game = board.Board()
    while True: #TODO change to not GAMEOVER
        game.display()
        game.player_turn()
    
if __name__ == '__main__':
    main()