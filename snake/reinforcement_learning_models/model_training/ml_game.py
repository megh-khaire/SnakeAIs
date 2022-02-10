import pygame
import numpy as np
from snake.main.point import Point
from snake.main.game import Game
from snake.resources.constants import BLOCK_SIZE, FIXED_AUTO_SPEED, REWARD, MAX_ITR
from snake.resources.directions import Direction, STRAIGHT, TURN_LEFT, TURN_RIGHT

pygame.init()
font = pygame.font.SysFont('arial', 25)


class ReinforcementLearning(Game):
    def __init__(self, game_type):
        Game.__init__(self, game_type)
        self.frame_iteration = 0

    def get_next_head(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)
        if np.array_equal(action, STRAIGHT):
            new_dir = clock_wise[index]  # no change
        elif np.array_equal(action, TURN_RIGHT):
            next_index = (index + 1) % 4
            new_dir = clock_wise[next_index]  # right turn (r -> d -> l -> u -> r)
        elif np.array_equal(action, TURN_LEFT):
            next_index = (index - 1) % 4
            new_dir = clock_wise[next_index]  # left turn (r -> u -> l -> d -> r)
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        return Point(x, y)

    def main(self, action):
        self.frame_iteration += 1
        reward = 0
        # Checking user input
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Moving snake
        self.head = self.get_next_head(action)
        self.snake.insert(0, self.head)
        # Check if snake has hit something

        if self.detect_collision() or self.frame_iteration > MAX_ITR + (REWARD * self.score):
            reward = REWARD * -1
            return True, reward, self.score

        # Check if snake has reached the food point and generate path to this new point
        if self.head == self.food:
            self.score += 1
            reward = REWARD + self.score
            self.generate_food()
        else:
            # Remove the last element from the snake's body as we have added a new head
            self.snake.pop()

        # Updating UI and Clock
        self.update_ui()
        self.clock.tick(FIXED_AUTO_SPEED)

        return False, reward, self.score
