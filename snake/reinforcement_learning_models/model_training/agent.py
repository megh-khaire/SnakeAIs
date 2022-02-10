import torch
import random
import numpy as np
from collections import deque

from snake.main.point import Point
from snake.resources.constants import BLOCK_SIZE
from snake.resources.directions import Direction
from snake.reinforcement_learning_models.model_training.ml_game import ReinforcementLearning
from model import Linear_QNet, QTrainer
from plotter import plot

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001
EPSILON_THRESHOLD = 80
RANDOMNESS_THRESHOLD = 200


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.detect_random_point_collision(point_r)) or
            (dir_l and game.detect_random_point_collision(point_l)) or
            (dir_u and game.detect_random_point_collision(point_u)) or
            (dir_d and game.detect_random_point_collision(point_d)),

            # Danger right
            (dir_u and game.detect_random_point_collision(point_r)) or
            (dir_d and game.detect_random_point_collision(point_l)) or
            (dir_l and game.detect_random_point_collision(point_u)) or
            (dir_r and game.detect_random_point_collision(point_d)),

            # Danger left
            (dir_d and game.detect_random_point_collision(point_r)) or
            (dir_u and game.detect_random_point_collision(point_l)) or
            (dir_r and game.detect_random_point_collision(point_u)) or
            (dir_l and game.detect_random_point_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y   # food down
        ]
        return np.array(state, dtype=bool)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff between exploration and exploitation
        self.epsilon = EPSILON_THRESHOLD - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, RANDOMNESS_THRESHOLD) < self.epsilon:
            move = random.randint(0, len(final_move) - 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = ReinforcementLearning("RL")
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)
        # perform move and get new state
        done, reward, score = game.main(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory and plot results
            game.reset()
            game.frame_iteration = 0
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game: ', agent.n_games, 'Score: ', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
