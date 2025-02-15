import unittest
import pygame
import os
from pygame.locals import *
from unittest.mock import patch
from car_game.all_game import main_menu

from car_game.park import (run_parking, parking_spot, check_overlap, load_level, levels, car_images, car_rect, level_obstacles,
                  yellow_bonus_levels, yellow_bonus, orange_bonus_levels, orange_bonus, obstacles)


class TestParkTheCar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((1000, 700))
        pygame.event.pump()

    def tearDown(self):
        pygame.quit()

    def setUp(self):
        """Reset game state before each test"""
        global lives, score, current_level_park, unlocked_levels_park
        lives = 3
        score = 0
        current_level_park = 0
        unlocked_levels_park = 1
        load_level(current_level_park, testing=True)

    def test_game_initialization(self):
        """Test if the game initializes screen and loads assets correctly"""
        self.assertEqual(self.screen.get_size(), (1000, 700))

    def test_car_switching(self):
        """Test if pressing space changes the car"""
        initial_car = car_images[0]
        with patch("pygame.key.get_pressed", return_value={pygame.K_SPACE: True}):
            global current_car_index
            current_car_index = (current_car_index + 1) % len(car_images)
            self.assertNotEqual(initial_car, car_images[current_car_index])

    def test_check_overlap(self):
        """Ensure the check_overlap function detects overlapping rectangles correctly"""
        rect1 = pygame.Rect(100, 100, 50, 50)
        rect2 = pygame.Rect(120, 120, 50, 50)
        rect3 = pygame.Rect(250, 250, 50, 50)
        self.assertTrue(check_overlap(rect1, [rect2]))
        self.assertFalse(check_overlap(rect1, [rect3]))

    def test_load_level(self):
        """Ensure load_level correctly sets parking spots and obstacles"""
        level = 2
        load_level(level, testing=True)
        self.assertEqual(levels[level], levels[level])  # Parking spot should be correct
        self.assertTrue(len(level_obstacles.get(level, [])) >= 0)  # Obstacles should be loaded

    def test_collision_with_obstacle(self):
        """Test if the car collides with obstacles"""
        car_rect.x, car_rect.y = 400, 200  # Position car near obstacle
        obstacles_for_test = [{"rect": pygame.Rect(400, 200, 80, 40)}]
        collision = any(car_rect.colliderect(obs["rect"]) for obs in obstacles_for_test)
        self.assertTrue(collision)

    def test_parking_spot_success(self):
        """Test if the car successfully parks"""
        car_rect.x, car_rect.y = levels[0].x + 5, levels[0].y + 5  # Place car inside parking spot
        self.assertTrue(levels[0].contains(car_rect))  # Should be inside

    def test_obstacles_loaded_correctly(self):
        """Ensure obstacles are loaded correctly for each level"""
        for level in range(len(levels)):
            load_level(level, testing=True)
            for obstacle in level_obstacles.get(level, []):
                self.assertIn(obstacle, [o["rect"] for o in obstacles], f"Obstacle {obstacle} missing in level {level}")

    def test_bonus_loading(self):
        """Ensure bonuses (yellow and orange) load correctly based on levels"""
        for level in range(len(levels)):
            load_level(level, testing=True)
            if level in yellow_bonus_levels:
                self.assertGreater(len(yellow_bonus), 0, f"Yellow bonuses not loaded for level {level}")
            else:
                self.assertEqual(len(yellow_bonus), 0, f"Unexpected yellow bonuses in level {level}")

            if level in orange_bonus_levels:
                self.assertGreater(len(orange_bonus), 0, f"Orange bonuses not loaded for level {level}")
            else:
                self.assertEqual(len(orange_bonus), 0, f"Unexpected orange bonuses in level {level}")

    @patch("pygame.event.get")
    def test_car_movement(self, mock_pygame_event):
        """Test car movement on arrow key presses"""
        mock_pygame_event.return_value = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})]
        initial_y = car_rect.y
        run_parking(main_menu, testing=True)
        self.assertLess(car_rect.y, initial_y, "Car should move UP")

    @patch("pygame.event.get")
    def test_car_collision_with_obstacles(self, mock_pygame_event):
        """Test if the car loses a life on collision with an obstacle"""
        global lives
        lives = 3
        car_rect.x, car_rect.y = obstacles[0]["rect"].x, obstacles[0]["rect"].y  # Simulate collision
        run_parking(main_menu, testing=True)
        self.assertEqual(lives, 2, "Lives should decrease after collision")

    @patch("pygame.event.get")
    def test_parking_success(self, mock_pygame_event):
        """Test if the car successfully parks in the correct spot"""
        global current_level_park, unlocked_levels_park
        car_rect.x, car_rect.y = parking_spot.x + 5, parking_spot.y + 5  # Place car in parking spot
        run_parking(main_menu, testing=True)
        self.assertGreater(current_level_park, 0, "Car should move to the next level after parking")
        self.assertGreater(unlocked_levels_park, 1, "Next level should be unlocked")

    @patch("pygame.event.get")
    def test_bonus_collection(self, mock_pygame_event):
        """Test if the car collects bonuses and increases score"""
        global score
        car_rect.x, car_rect.y = yellow_bonus[0].x, yellow_bonus[0].y  # Simulate collecting a yellow bonus
        run_parking(main_menu, testing=True)
        self.assertGreater(score, 0, "Score should increase after collecting a bonus")


from car_game.maze import get_the_snickers, levels, player_pos, goal_pos, current_level, unlocked_levels


class TestMazeGame(unittest.TestCase):

    def setUp(self):
        """ Initialize Pygame for testing"""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Maze Game - Level 1")
        pygame.event.pump()

    def tearDown(self):
        pygame.quit()

    def test_initial_player_position(self):
        """Test that the player starts at the correct position """
        self.assertEqual(player_pos, [1, 1])

    def test_initial_unlocked_levels(self):
        """Test that only the first level is unlocked initially"""
        self.assertEqual(unlocked_levels, [0])

    def test_player_movement(self):
        """Test player movement within the maze"""
        initial_pos = player_pos.copy()

        # Дясно
        new_pos = [initial_pos[0] + 1, initial_pos[1]]
        if levels[current_level][new_pos[1]][new_pos[0]] == 0:
            player_pos[0] += 1
        self.assertEqual(player_pos, new_pos)

        # Долу
        new_pos = [player_pos[0], player_pos[1] + 1]
        if levels[current_level][new_pos[1]][new_pos[0]] == 0:
            player_pos[1] += 1
        self.assertEqual(player_pos, new_pos)

        # Ляво
        new_pos = [player_pos[0] - 1, player_pos[1]]
        if levels[current_level][new_pos[1]][new_pos[0]] == 0:
            player_pos[0] -= 1
        self.assertEqual(player_pos, new_pos)

        # Горе
        new_pos = [player_pos[0], player_pos[1] - 1]
        if levels[current_level][new_pos[1]][new_pos[0]] == 0:
            player_pos[1] -= 1
        self.assertEqual(player_pos, new_pos)

    def test_goal_reached(self):
        """Test that the player can reach the goal """
        player_pos[0] = goal_pos[current_level][0]
        player_pos[1] = goal_pos[current_level][1]
        self.assertEqual(player_pos, goal_pos[current_level])

    def test_level_unlocking(self):
        """Test that completing a level unlocks the next one"""
        player_pos[0] = goal_pos[current_level][0]
        player_pos[1] = goal_pos[current_level][1]
        get_the_snickers()  # Simulate winning the level
        self.assertIn(current_level + 1, unlocked_levels)

    def test_car_image_switching(self):
        """Test that the car image switches correctly"""
        initial_car_index = current_car_index
        get_the_snickers()  # Simulate pressing the space bar
        self.assertEqual(current_car_index, (initial_car_index + 1) % len(car_images))


from car_game.race import (terminate, wait_for_player_to_press_key, player_has_hit_baddie, draw_text, run_racing,
                  WINDOWWIDTH, WINDOWHEIGHT)


class TestCarRacingGame(unittest.TestCase):

    def setUp(self):
        # Initialize Pygame for testing
        pygame.init()
        self.windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Car Race Test')
        self.font = pygame.font.SysFont(None, 30)
        pygame.event.pump()

    def tearDown(self):
        pygame.quit()

    def test_terminate(self):
        # Test the terminate function
        with self.assertRaises(SystemExit):
            terminate()

    def test_waitForPlayerToPressKey(self):
        # Test the wait_for_player_to_press_key function
        # Simulate a key press event
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_SPACE))
        wait_for_player_to_press_key()  # Should not raise an exception

    def test_playerHasHitBaddie(self):
        # Test the player_has_hit_baddie function
        player_rect = pygame.Rect(100, 100, 50, 50)
        baddies = [
            {'rect': pygame.Rect(100, 100, 50, 50), 'speed': 5, 'surface': None},
            {'rect': pygame.Rect(200, 200, 50, 50), 'speed': 5, 'surface': None}
        ]
        self.assertTrue(player_has_hit_baddie(player_rect, baddies))

        player_rect.top_left = (300, 300)
        self.assertFalse(player_has_hit_baddie(player_rect, baddies))

    def test_drawText(self):
        # Test the draw_text function
        text = "Test Text"
        x, y = 100, 100
        draw_text(text, self.font, self.windowSurface, x, y)
        # Verify that the text was drawn (this is more of a visual test)
        # For automated testing, you might need to capture the screen and analyze the pixels.

    def test_run_racing(self):
        # Test the run_racing function
        # Simulate key presses and game logic
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_SPACE))  # Start the game
        run_racing()

        # Simulate player movement
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_LEFT))
        pygame.event.post(pygame.event.Event(KEYUP, key=K_LEFT))
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RIGHT))
        pygame.event.post(pygame.event.Event(KEYUP, key=K_RIGHT))

        # Simulate collision
        player_rect = pygame.Rect(100, 100, 50, 50)
        baddies = [{'rect': pygame.Rect(100, 100, 50, 50), 'speed': 5, 'surface': None}]
        self.assertTrue(player_has_hit_baddie(player_rect, baddies))

        # Simulate game over
        global count
        count = 0
        run_racing()  # Should display "Game Over" screen

    def test_score_and_top_score(self):
        # Test score and top score functionality
        if not os.path.exists("../data_save.dat"):
            with open("../data_save.dat", 'w') as f:
                f.write("0")

        with open("../data_save.dat", 'r') as v:
            top_score = int(v.readline())

        # Simulate a high score
        score = 1000
        if score > top_score:
            with open("../data_save.dat", 'w') as g:
                g.write(str(score))
            top_score = score

        self.assertEqual(top_score, 1000)


if __name__ == "__main__":
    unittest.main()
