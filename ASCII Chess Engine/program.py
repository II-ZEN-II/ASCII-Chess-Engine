import board

def main():
    game = board.Board()
    while game.get_gameover() == False:
        game.display()
        game.player_turn()
        
    
if __name__ == '__main__':
    main()