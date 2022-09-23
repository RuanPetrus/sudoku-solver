# SUDOKU GENERATOR AND SOLVER

# How to run
Program was made using python 3.10.6  

The program can solve a sudoku game. Need to pass the path to the input file and the base of the game. Run the follow:  
```sh
python main.py sol <input_file> <base>
```
EX:  
```sh
python main.py sol example_board.txt 3
```

The program can generate a solvable board, need to pass the base of the game and the number of empty squares. Run the follow:  
```sh
python main.py gen <base> <number_of_empty_squares>
```
EX:  
```sh
python main.py gen 3 20
```

The program can generate a solvable board and solved, need to pass the base of the game and the number of empty squares. Run the follow:  
```sh
python main.py genAndSol <base> <number_of_empty_squares>
```
EX:  
```sh
python main.py genAndSol 3 20
```

# References
- [Sodoku_graph](https://en.wikipedia.org/wiki/Sudoku_graph)
- [Solving soduku smartly](https://youtu.be/LNeW8TpfCCg)
- [Python Soduku solver](https://youtu.be/G_UYXzGuqvM)
- [How to create a sudoku solver in python](https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python)
- [Computerphile](https://youtu.be/G_UYXzGuqvM)
