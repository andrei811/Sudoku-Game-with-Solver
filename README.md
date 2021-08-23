# Sudoku-Game-with-Solver
![img](https://raw.githubusercontent.com/andrei811/Sudoku-Game-with-Solver/master/Images/image.jpg)

You can play sudoku or you can let the computer solve it for you. The algorithm for solving the game uses backtracking technique to fill the blank spaces.

## Library instalation
The code execution requires the `pygame` library. The installation can be performed by running the following command in terminal.

```
pip install pygame
```

## Execute the game
Open the terminal and make sure that the working directory is `Sudoku-Game-with-Solver`. Make sure also that you have `python` installed on the machine. Then execute the following command:
```
python Sudoku/sudoku_GUI.py
```

## Aditional info
The `sudokumatrix.txt` stores the sudoku board. The `sudoku_text.py` file implements the backtracking algorithm for solving the game. The main file, `sudoku_GUI.py` uses the other files and implements a nice-looking GUI for the game.