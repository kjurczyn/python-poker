from os import kill, sep
from sys import path, exit
from pathlib import Path
from time import sleep
path[0] = str(Path(path[0]).parent)
from typing import List
from Poker.game import Game
from Poker.player import Player
from simple_term_menu import TerminalMenu
from threading import Event, Thread
from queue import Queue
from pokerbot import makeChoice
del path


def getNumInput(min_amount: int, max_amount: int) -> int:
    """Takes a keyboard input from the user and returns it if it meets all the conditions."""
    amount = None
    while True:
        user_input = input(f'Min amount{min_amount}, max amount {max_amount}. Amount must be multiple of 100. Enter amount:')
        try:
            amount = int(user_input)
            if amount % 100 == 0:
                break
            else:
                print('Amount is not multiple of 100.')
        except Exception:
            print('Input invalid.')
    return amount


def main():
    human_player = Player('You')
    main_game = Game([
        human_player,
        Player('Bot_John'),
        Player('Bot_Jane'),
        Player('Bot_Jack'),
        Player('Bot_Jill'),
        Player('Bot_Jake')
        ])

    current_player_queue = Queue(1)
    winner_queue = Queue(1)

    game_waiting_event = Event()
    game_continue_event = Event()

    game_thread = Thread(target=main_game.playGame, args=(game_waiting_event, game_continue_event, current_player_queue, winner_queue))
    game_thread.start()

    while game_thread.is_alive():
        game_waiting_event.wait()
        game_waiting_event.clear()
        print(main_game)
        if main_game.getSmallBlind() in main_game.getPlayers():
            print(f'{main_game.getSmallBlind().getName()} paid the ${100*main_game.getBlindMultiplier()} blind.')
        if main_game.getBigBlind() in main_game.getPlayers():
            print(f'{main_game.getBigBlind().getName()} paid the ${200*main_game.getBlindMultiplier()} blind.')
        game_continue_event.set()
        while winner_queue.empty():
            sleep(0.5)
            game_waiting_event.wait()
            game_waiting_event.clear()
            current_player: Player = current_player_queue.get()
            if current_player == human_player:
                print('Cards on table:')
                print(*main_game.getTable(), sep=' | ')
                print('Your Cards:')
                print(*current_player.getHand(), sep=' | ')
                print(f'Call amount: {main_game.getPots()[current_player.getCurrentPot()][0]}')
                print(f'Your money: {current_player.getMoney()}')
                options = main_game.getOptionsFor(current_player)
                player_menu = TerminalMenu(options)
                choice = player_menu.show()
                if choice is None:
                    print('Exiting game. Use Ctr+C to return to Bash.')
                    exit()
                elif options[choice] == 'Fold':
                    current_player.passRound()
                elif 'Call' in options[choice]:
                    main_game.bet(current_player, main_game.getPots()[current_player.getCurrentPot()][0])
                elif options[choice] == 'Raise':
                    main_game.bet(current_player, getNumInput(main_game.getPots()[current_player.getCurrentPot()][0],
                                  current_player.getMoney())-current_player.getCurrentBet())
                elif options[choice] == 'All In':
                    main_game.bet(current_player, current_player.getMoney())
            else:
                choice = makeChoice(current_player, main_game)
                # pass
                if choice[0] == 1:
                    current_player.passRound()
                    print(f'{current_player.getName()} folded.')
                # call
                elif choice[0] == 3:
                    main_game.bet(current_player, main_game.getPots()[current_player.getCurrentPot()][0]-current_player.getCurrentBet())
                    print(f'{current_player.getName()} called the bet.')
                # raise
                elif choice[0] == 4:
                    main_game.bet(current_player, choice[1])
                    print(f'{current_player.getName()} raised ${choice[1]}.')
                # all in
                elif choice[0] == 5:
                    main_game.bet(current_player, current_player.getMoney())
                    print(f'{current_player.getName()} went all in!')
                # check
                elif choice[0] == 2:
                    print(f'{current_player.getName()} checked.')
            game_continue_event.set()
        game_waiting_event.wait()
        game_waiting_event.clear()
        round_winners = winner_queue.get()
        if len(round_winners) == 1:
            print('Round won by', *round_winners[0], sep=' ')
        else:
            print('Main pot won by', *round_winners[0], sep=' ')
            for i in range(1, len(round_winners)):
                print(f'Side pot {i} won by:', *round_winners[i], sep=' ')
        game_continue_event.set()
    game_winner = winner_queue.get()
    print(f'{game_winner} won the game!')


if __name__ == '__main__':
    main()
