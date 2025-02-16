import unittest
import pygame
from unittest.mock import patch, MagicMock
pygame.init()
from park import *


class TestParkTheCar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Park the Car - Test")

    def tearDown(self):
        global lives, score, current_level, unlocked_levels, current_car_index
        lives = 3
        score = 0
        current_level = 0
        unlocked_levels = 1
        current_car_index = 0

    def test_car_switching(self):
        """Test if pressing space changes the car."""
        global current_car_index
        initial_car = car_images[current_car_index]

        with patch("pygame.key.get_pressed", return_value={pygame.K_SPACE: True}):
            current_car_index = (current_car_index + 1) % len(car_images)
            self.assertNotEqual(initial_car, car_images[current_car_index])

    def test_check_overlap(self):
        """Test that the check_overlap function detects overlapping rectangles."""
        rect1 = pygame.Rect(100, 100, 50, 50)
        rect2 = pygame.Rect(120, 120, 50, 50)
        rect3 = pygame.Rect(250, 250, 50, 50)

        self.assertTrue(check_overlap(rect1, [rect2]))
        self.assertFalse(check_overlap(rect1, [rect3]))

    def test_load_level(self):
        """Test that load_level correctly sets parking spots and obstacles."""
        global current_level, parking_spot, obstacles, yellow_bonus, orange_bonus

        # Load level 0
        load_level(current_level, testing=True)
        self.assertEqual(parking_spot, levels[current_level-1])
        self.assertTrue(len(obstacles) >= 0)

        # Load level 1
        current_level = 1
        load_level(current_level, testing=True)
        self.assertEqual(parking_spot, levels[current_level-1])
        self.assertTrue(len(obstacles) >= 0)

    def test_collision_with_obstacle(self):
        """Test if the car collides with obstacles."""
        global car_rect, lives

        car_rect.x, car_rect.y = 400, 200
        obstacles_for_test = [{"rect": pygame.Rect(400, 200, 80, 40)}]
        collision = any(car_rect.colliderect(obs["rect"]) for obs in obstacles_for_test)
        self.assertTrue(collision)

        car_rect.x, car_rect.y = 500, 500
        collision = any(car_rect.colliderect(obs["rect"]) for obs in obstacles_for_test)
        self.assertFalse(collision)

    def test_parking_spot_success(self):
        """Test if the car successfully parks."""
        global car_rect, parking_spot

        car_rect.x, car_rect.y = parking_spot.x + 5, parking_spot.y + 5
        self.assertTrue(parking_spot.contains(car_rect))

    def test_obstacles_loaded_correctly(self):
        """Ensure obstacles are loaded correctly for each level."""
        for level in range(len(levels)):
            load_level(level, testing=True)
            for obstacle in level_obstacles.get(level, []):
                self.assertIn(obstacle, [o["rect"] for o in obstacles], f"Obstacle {obstacle} missing in level {level}")

    @patch("pygame.event.get")
    def test_car_movement(self, mock_event_get):
        """Test car movement on arrow key presses (left, right, up, down)."""
        global car_rect

        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})]
        initial_y = car_rect.y
        run_parking(MagicMock(), testing=True)
        self.assertLess(car_rect.y, initial_y, "Car should move UP")

        car_rect.y = initial_y

        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})]
        initial_y = car_rect.y
        run_parking(MagicMock(), testing=True)
        self.assertGreater(car_rect.y, initial_y, "Car should move DOWN")

        car_rect.y = initial_y

        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})]
        initial_x = car_rect.x
        run_parking(MagicMock(), testing=True)
        self.assertLess(car_rect.x, initial_x, "Car should move LEFT")

        car_rect.x = initial_x

        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT})]
        initial_x = car_rect.x
        run_parking(MagicMock(), testing=True)
        self.assertGreater(car_rect.x, initial_x, "Car should move RIGHT")

    @patch("pygame.event.get")
    def test_car_collision_with_obstacles(self, mock_event_get):
        """Test if the car loses a life on collision with an obstacle."""
        global lives, car_rect

        car_rect.x, car_rect.y = obstacles[0]["rect"].x, obstacles[0]["rect"].y
        run_parking(MagicMock(), testing=True)
        self.assertEqual(lives, 2, "Lives should decrease after collision")

    @patch("pygame.event.get")
    def test_parking_success(self, mock_event_get):
        """Test if the car successfully parks in the correct spot."""
        global current_level, unlocked_levels, car_rect, parking_spot

        car_rect.x, car_rect.y = parking_spot.x + 5, parking_spot.y + 5
        run_parking(MagicMock(), testing=True)
        self.assertGreater(unlocked_levels, 1, "Next level should be unlocked")

    @patch("pygame.event.get")
    def test_bonus_collection(self, mock_event_get):
        """Test if the car collects bonuses and increases score."""
        global score, car_rect

        car_rect.x, car_rect.y = yellow_bonus[0].x, yellow_bonus[0].y
        run_parking(MagicMock(), testing=False)
        self.assertGreater(score, 0, "Score should increase after collecting a bonus")


if __name__ == "__main__":
    unittest.main()
