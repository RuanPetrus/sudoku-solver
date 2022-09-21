# SUDOKU GENERATOR AND SOLVER

# How to run
Program was made using python 3.10.6  

The program can check if a game is a valid need to pass the path to the input file and the base of the game. Run the follow:  
```sh
python main.py check_valid <input_file> <base
```
EX:  
```sh
python main.py check_valid example_board.txt 3
```

The program can generate a solvable board and solve, need to pass the base of the game and the number of empty squares. Run the follow:  
```sh
python main.py solve <base> <number_of_empty_squares>
```
EX:  
```sh
python main.py solve 3 20
```

# References
- [Sodoku_graph](https://en.wikipedia.org/wiki/Sudoku_graph)
- [Solving soduku smartly](https://youtu.be/LNeW8TpfCCg)
- [Python Soduku solver](https://youtu.be/G_UYXzGuqvM)
- [How to create a sudoku solver in python](https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python)
