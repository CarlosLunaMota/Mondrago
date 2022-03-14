# Mondrago
A brute force solver for the Mondrago board game


This repository contains two Python scripts: 

* `Mondrago.py` generates a 329,5 Mb file called `MONDRAGO_DATABASE.py` (and the smaller `MONDRAGO_STATS.txt`, which contains the depth distribution of all Mondrago's positions).
* `Mondrago_Explorer.py` mines the `MONDRAGO_DATABASE.py` to generate the other files that you can find here.


The outputs of `Mondrago_Explorer.py` are:

* `MONDRAGO_INITIAL_POSITIONS.txt` contains all symmetrical positions of Mondrago (i.e. alternative starting positions).
* `MONDRAGO_SAFEST_DRAWS.txt` contains the 56 *safe* draws of Mondrago (i.e. positions with no losing moves and no winning moves).
* `MONDRAGO_DEEPEST_POSITIONS.txt` contains the 7 deepest forced wins (i.e. first player wins in 75 plies with perfect play).
* `MONDRAGO_PUZZLES_XXX.txt` contains positions with a single winning move, no draw moves and, at least, 19 losing moves. EASY means depth=3, NORMAL means depth=5, DIFFICULT means depth=7 and VERY_DIFFICULT means depth=9.
