import random
import pygame
import numpy as np
from snake.resources.constants import WIDTH, HEIGHT, BLOCK_SIZE, OBSTACLE_THRESHOLD, INITIAL_SPEED, SPEED_THRESHOLD, SPEEDUP
from snake.resources.colors import WHITE, RED, BLUE, GREEN, BLACK
from snake.resources.directions import Direction, STRAIGHT, TURN_LEFT, TURN_RIGHT

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, point) : 
        if self.__class__ != point.__class__:
            return False
        return self.__dict__ == point.__dict__

    # Function to plot draw point
    def plot(self, display, color):
        pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.direction = Direction.UP
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles = []
        self.food = None
        self.frame_iteration = 0
        self.generate_obstacles()
        self.place_food()

    # Function to reset the games state
    def reset(self):
        self.direction = Direction.UP
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles = []
        self.food = None
        self.frame_iteration = 0
        self.generate_obstacles()
        self.place_food()

    # Function to randomly place food in the game
    def place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake or self.food in self.obstacles:
            self.place_food()

    # Function to randomly generate obstacles in the game
    def generate_obstacles(self):
        for i in range(0, OBSTACLE_THRESHOLD):
            x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
            y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            obstacle = Point(x, y)
            if obstacle not in self.snake: 
                self.obstacles.append(obstacle)
            
    def move_snake(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)
        if np.array_equal(action, STRAIGHT):
            new_dir = clock_wise[index] # no change
        elif np.array_equal(action, TURN_RIGHT):
            next_index = (index+1)%4
            new_dir = clock_wise[next_index] # right turn (r -> d -> l -> u -> r)
        elif np.array_equal(action, TURN_LEFT):
            next_index = (index-1)%4
            new_dir = clock_wise[next_index] # left turn (r -> u -> l -> d -> r)
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
        self.head = Point(x, y)

    def is_collision(self, point=None):
        if not point:
            point = self.head
        # Checking boundary condition
        if point.x > self.width - BLOCK_SIZE or point.x < 0 or point.y > self.height - BLOCK_SIZE or point.y < 0:
            return True
        # Checking if the snake hit itself
        if point in self.snake[1:]:
            return True
        # Checking if the snake hit an obstacle
        if point in self.obstacles:
            return True

    # Function to update game ui
    def update_ui(self):
        self.display.fill(BLACK)
        # Drawing snake's body
        for point in self.snake:
            point.plot(self.display, GREEN)
        # Drawing snake's head
        self.head.plot(self.display, WHITE)
        # Drawing obstacles
        for point in self.obstacles:
            point.plot(self.display, RED)
        # Drawing food
        self.food.plot(self.display, BLUE)
        # Display score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def process(self, action):
        self.frame_iteration += 1
        reward = 0
        # Checking user input
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Moving snake
        self.move_snake(action)
        self.snake.insert(0, self.head)
        # Check if snake has hit something
        
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            reward = -10
            return True, reward, self.score

        # Check if snake has reached the food
        # if self.head.position_check(self.food):
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            #Remove the last element from the snake's body as we have added a new head
            self.snake.pop()

        # Updating UI and Clock
        speed = INITIAL_SPEED + SPEED_THRESHOLD
        self.update_ui()
        self.clock.tick(speed)

        return False, reward, self.score
