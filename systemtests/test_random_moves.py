from game import Game
from player import Computer, Human
import unittest
from time import sleep
import threading

class TestGame(unittest.TestCase):
    @staticmethod
    def quit_on_mate(game, ai1, ai2):
        def is_mate():
            for i in range(500):
                if 'mate' not in game.game_state:
                    sleep(0.5)
                else:
                    return
            raise RuntimeError('Timeout: Game did not end')

        thread = threading.Thread(target=is_mate)
        thread.start()
        thread.join()
        ai1.quit()
        ai2.quit()
        game.quit()
        sleep(0.5)


    def test_random(self):
        try:
            for i in range(2):
                print("------ game %d ------" % (i+1))
                game = Game()
                ai1 = Computer(game=game, color='black')
                ai2 = Computer(game=game, color='white')
                thread1 = ai1.start()
                thread2 = ai2.start()
            
                self.quit_on_mate(game, ai1, ai2)
                self.assertFalse(thread1.is_alive())
                self.assertFalse(thread2.is_alive())
        except Exception as e:
            ai1.quit()
            ai2.quit()
            game.quit()
            raise e


        
