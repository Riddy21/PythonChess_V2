from game import Game
from player import Computer, Human
import unittest
from time import sleep
from utils import *
import random
from gui import ChessboardGUI

class TestRandomGame(unittest.TestCase):
    def setUp(self):
        self.failed = False

    def test_undo(self):
        @run_in_thread
        def undo_on_mate(game, ai1, ai2, num_undos=5):
            # FIXME: Add function to quit if the players throw an exception using the ai1.failed
            try:
                for i in range(1000):
                    print(game.game_state)
                    if 'mate' not in game.game_state:
                        sleep(0.5)
                    else:
                        print('YO')
                        if num_undos > 0:
                            ai1.undo_move(random.randint(1, 10))
                            num_undos -= 1
                        else:
                            return
            finally:
                self.failed = True
                raise RuntimeError('Timeout: Game did not end')

        try:
            # Let game play till stalemate or checkmate
            game = Game()
            game.set_board(config_file="Presets/almost_mate.txt")
            ai1 = Computer(game=game, color='black')
            ai2 = Computer(game=game, color='white')
            #gui = ChessboardGUI(game, ai1, ai2, interactive=False)
            #gui.run()
            thread1 = ai1.start()
            thread2 = ai2.start()
            
            thread = undo_on_mate(game, ai1, ai2, num_undos=5)
            thread.join()
            ai1.quit()
            ai2.quit()
            #gui.quit()
            game.quit()
            sleep(5)
            self.assertFalse(thread1.is_alive())
            self.assertFalse(thread2.is_alive())
            self.assertFalse(self.failed)
            print("undo on mate test is success")
        except Exception as e:
            ai1.quit()
            ai2.quit()
            #gui.quit()
            game.quit()
            raise e

    #def test_random_undo(self):
    #    @run_in_thread
    #    def random_undo_thread(game, ai1, ai2):
    #        # FIXME: Add function to quit if the players throw an exception using the ai1.failed
    #        try:
    #            for i in range(1000):
    #                if 'mate' not in game.game_state:
    #                    sleep(random.random()*20)
    #                    ai1.undo_move(random.randint(1, 3))
    #                else:
    #                    return
    #        finally:
    #            self.failed = True
    #            raise RuntimeError('Timeout: Game did not end')
    #    try:
    #        # Let game play till stalemate or checkmate
    #        game = Game()
    #        ai1 = Computer(game=game, color='black')
    #        ai2 = Computer(game=game, color='white')
    #        gui = ChessboardGUI(game, ai1, ai2, interactive=False)
    #        #gui.run()
    #        thread1 = ai1.start()
    #        thread2 = ai2.start()
    #        
    #        thread = random_undo_thread(game, ai1, ai2)
    #        thread.join()
    #        ai1.quit()
    #        ai2.quit()
    #        game.quit()
    #        #gui.quit()
    #        sleep(5)
    #        self.assertFalse(thread1.is_alive())
    #        self.assertFalse(thread2.is_alive())
    #        self.assertFalse(self.failed)
    #        print("Random undo test is successful")
    #    except Exception as e:
    #        ai1.quit()
    #        ai2.quit()
    #        #game.quit()
    #        gui.quit()
    #        raise e
