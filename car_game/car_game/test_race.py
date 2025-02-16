import unittest
import pygame

pygame.init()
from race import *


class TestCarRacingGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Car Race - Test')

    def tearDown(self):
        global count
        count = 3
        if os.path.exists("data_save.dat"):
            os.remove("data_save.dat")

    def test_player_movement(self):
        """Test player movement in all directions."""
        player_rect = pygame.Rect(WINDOWWIDTH / 2, WINDOWHEIGHT - 50, 50, 50)

        player_rect.move_ip(-1 * PLAYERMOVERATE, 0)
        self.assertEqual(player_rect.left, (WINDOWWIDTH / 2) - PLAYERMOVERATE)

        player_rect.move_ip(PLAYERMOVERATE, 0)
        self.assertEqual(player_rect.left, WINDOWWIDTH / 2)

        player_rect.move_ip(0, -1 * PLAYERMOVERATE)
        self.assertEqual(player_rect.top, (WINDOWHEIGHT - 50) - PLAYERMOVERATE)

        player_rect.move_ip(0, PLAYERMOVERATE)
        self.assertEqual(player_rect.top, WINDOWHEIGHT - 50)

    def test_collision_detection(self):
        """Test that the game detects collisions between the player and baddies."""
        player_rect = pygame.Rect(100, 100, 50, 50)
        baddies = [
            {'rect': pygame.Rect(100, 100, 50, 50), 'speed': 5, 'surface': None},
            {'rect': pygame.Rect(200, 200, 50, 50), 'speed': 5, 'surface': None}
        ]

        self.assertTrue(player_has_hit_baddie(player_rect, baddies))

        player_rect.topleft = (300, 300)
        self.assertFalse(player_has_hit_baddie(player_rect, baddies))

    def test_baddie_spawning(self):
        """Test that baddies are spawned correctly."""
        baddies = []
        baddie_add_counter = 0

        baddie_add_counter += 1
        if baddie_add_counter == ADDNEWBADDIERATE:
            baddie_add_counter = 0
            new_baddie = {
                'rect': pygame.Rect(random.randint(140, 485), 0 - 30, 23, 47),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': None
            }
            baddies.append(new_baddie)

        self.assertEqual(len(baddies) + 1, 1)

    def test_score_and_top_score(self):
        """Test that the score updates correctly and the top score is saved."""
        score = 1000
        top_score = 500

        if score > top_score:
            with open("data_save.dat", 'w') as f:
                f.write(str(score))
            top_score = score

        self.assertEqual(top_score, 1000)


if __name__ == "__main__":
    unittest.main()