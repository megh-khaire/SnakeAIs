<div id="top"></div>

# SnakeAIs

SnakeAIs (`Snakeyes`) is a recreation of the famous snake game using Python( famous for those who have witnessed the keypad era of mobile phones).
Traditionally in this game, a player assumes the role of a snake that has to manoeuvre around a grid to collect food and also avoid hitting obstacles in the process.
As the game progresses and the snake collects more food, its speed and size increase making it difficult for the player to efficiently manoeuvre the snake.
The objective here is to collect as many food items as possible before colliding with the obstacles, the walls of the grid or any part of the snake itself.

SnakeAIs puts a twist on the traditional snake game by using various `state-space search algorithms` that generate paths for the snake to traverse the grid and collect food.
The idea behind this project was to understand how these algorithms work by applying them to a game for better visualization and comparison.
The ultimate objective is to create gamified informational website for explaining each of these state-space algorithms though examples based on the game.


![Game Demo](https://github.com/megh-khaire/SnakeAIs/blob/main/images/demo.gif)

<!-- TABLE OF CONTENTS -->
<details>
      <summary>Table of Contents</summary>
      <ol>
            <li><a href="#installation">Installation</a></li>
            <li><a href="#usage">Usage</a></li>
            <li><a href="#modifications">Modifications</a></li>
            <li><a href="#roadmap">Roadmap</a></li>
            <li><a href="#contributing">Contributing</a></li>
            <li><a href="#license">License</a></li>
            <li><a href="#acknowledgments">Acknowledgments</a></li>
      </ol>
</details>

## Installation

- Make sure you have python installed.
- It is recommended to setup a new virtual environment before running the    project.
- Clone the repository and move into the project directory i.e `SnakeAIs`:

      git clone https://github.com/megh-khaire/SnakeAIs.git
      cd SnakeAIs


- Use the following command to install the required modules for running this project:
    - Using pip:

          pip install -r requirements.txt
    - Using conda:

          conda install --file requirements.txt

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

- To start the game move into the `snake` directory and run the `main.py` file:

      cd snake
      python main.py "bfs"
- The `main.py` file accepts a command line argument through which we can specift the type of algorithm the snake will use for traversal.
- Refer the following list to get the arguments required for using any of the currently supported algorithms:

<center>

| Algortihm | Argument |
| --------------- | --------------- |
| Random Search | `random` |
| Breadth First Search | `bfs` |
| Depth First Search | `dfs` |
| Hill Climing | `simple_hc` |
| Steepest Ascent Hill Climing | `steepest_ascent_hc` |
| Stochastic Hill Climing | `stochastic_hc` |
| Best First Seach | `bestfs` |
| A* Search | `a_star` |

</center>

- To play the game yourself you can use the following command:

        python main.py "human"

_Note: The random search algorithm moves the snake randomly throught the state-space and also avoids obstacles while doing so resulting in an endless loop._

<p align="right">(<a href="#top">back to top</a>)</p>

## Modifications

- `snake\resources\constants.py` defines constants that determine the rate at which the difficulty of the game will increase as the game progresses.
- To increase the difficulty of the game the speed of the game is increased by increasing the framerate.
- Following are the constants defined under `constants.py` that are used to manipulate the difficulty level of the game.
  - `INITIAL_SPEED` is the initial framerate when the game starts.
  - `SPEEDUP` is the rate at which the framerate increases after the snake accumulates a fixed threshold of points.
  - `SPEED_THRESHOLD` defines the number of food points the snake has to collect before speedup.
  - `FIXED_AUTO_SPEED` is the maximum framerate for the game, this is the maximum difficulty level.
  It is also the framerate at which the game runs when the snake while using the search algorithm.
- `snake\resources\colors.py` defines color constants used throughtout the game. These colors can be modified to change the color of the grid, snake, food and obstacles.

_Note: The difficulty configurations are only applicable when the user controls the snake's action. In cases where the algorithm controls the snake a fixed difficulty rate (FIXED_AUTO_SPEED) is used._

<p align="right">(<a href="#top">back to top</a>)</p>

## Roadmap

This project is currently under active development. In the near future, I plan to implement the following algorithms:
- Hamiltonian Cycle
- Reinforcement Learning
- Evolutionary Algorithms
- Genetic Algorithm combined with Deep Learning

After implementing these algorithms the next step will be to analyze their performance and start work on the gamified informational website, as mentined above that is the ultimate goal of this project.

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributing

Do you like the project or have new ideas? You are welcome to join the project. For small changes, you can drop in pull requests. For major changes, please open an issue first to discuss what you would like to change.

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the Apache License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

Earlier the scope of the projects was just restricted to the exploration of state-space search algorithms. A big thanks to the [Python Engineer](https://www.youtube.com/c/PythonEngineer) for making [this amazing tutorial](https://youtube.com/playlist?list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV) on Reinforcement learning that has now inspired me to explore Machine Learning techniques in my quest for developing the smartest Snake AI. Stay tuned for ore updates :).

<p align="right">(<a href="#top">back to top</a>)</p>
