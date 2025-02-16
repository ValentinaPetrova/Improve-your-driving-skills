import unittest
from unittest.mock import MagicMock, patch
import pygame
pygame.init()

from maze import *

class TestMazeGame(unittest.TestCase):

    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    def setUp(self, mock_set_mode, mock_set_caption):
        """Initialize mocks to avoid opening the actual game window"""
        pygame.event.pump = MagicMock()
        self.mock_get_snickers = MagicMock(side_effect=get_the_snickers)
        player_pos[:] = [1, 1]
    def tearDown(self):
        # pygame.quit()
        pass

    def test_initial_player_position(self):
        """Test that the player starts at the correct position"""
        self.assertEqual(player_pos, [1, 1])

    def test_initial_unlocked_levels(self):
        """Test that only the first level is unlocked initially"""
        self.assertEqual(unlocked_levels, [0])

    def test_player_movement(self):
        """Test player movement within the maze"""
        initial_pos = player_pos.copy()

        new_pos = [initial_pos[0] + 1, initial_pos[1]]
        if levels[current_level][new_pos[1]][new_pos[0]] == 0 and pygame.event == pygame.K_RIGHT:
            player_pos[0] += 1
        self.assertEqual(player_pos, new_pos)

        new_pos = [player_pos[0], player_pos[1] + 1]
        if levels[current_level][new_pos[1]][new_pos[0]] == 0 and pygame.event == pygame.K_DOWN:
            player_pos[1] += 1
        self.assertEqual(player_pos, new_pos)

        new_pos = [player_pos[0] - 1, player_pos[1]]
        if levels[current_level][new_pos[1]][new_pos[0]] == 0 and pygame.event == pygame.K_LEFT:
            player_pos[0] -= 1
        self.assertEqual(player_pos, new_pos)

        new_pos = [player_pos[0], player_pos[1] - 1]
        if levels[current_level][new_pos[1]][new_pos[0]] == 0 and pygame.event == pygame.K_UP:
            player_pos[1] -= 1
        self.assertEqual(player_pos, new_pos)

    @patch("maze.get_the_snickers", new_callable=MagicMock)
    def test_level_unlocking(self, mock_get_snickers):
        """Test that completing a level unlocks the next one"""
        mock_get_snickers()
        player_pos[0], player_pos[1] = goal_pos[current_level]
        self.assertIn(current_level + 1, unlocked_levels)

    @patch("maze.get_the_snickers", new_callable=MagicMock)
    def test_car_image_switching(self, mock_get_snickers):
        """Test that the car image switches correctly"""
        initial_car_index = current_car_index
        mock_get_snickers()
        self.assertEqual(current_car_index, (initial_car_index + 1) % len(car_images))


if __name__ == "__main__":
    unittest.main()
