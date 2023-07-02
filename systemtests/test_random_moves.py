from game import Game
from player import Computer, Human
import unittest

class TestGame(unittest.TestCase):
    def test_random(self):
        for i in range(5):
            print("------ game %d ------" % (i+1))
            game = Game()
            ai1 = Computer(game=game, color='black')
            ai2 = Computer(game=game, color='white')
            thread1 = ai1.start()
            thread2 = ai2.start()
        
            thread1.join()
            thread2.join()
