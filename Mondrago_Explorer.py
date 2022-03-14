
#######################################################################
#                                                                     #
# MONDRAGO EXPLORER: Data-mining script for the MONDRAGO_DATABASE.py  #
#                                                                     #
# Author:  Carlos Luna-Mota (https://github.com/CarlosLunaMota)       #
# Version: 2022-03-14                                                 #
# License: The Unlicense                                              #
#                                                                     #
#######################################################################


### BOARD TOPOLOGY #############################################################

#    0  1  2  3  4
#    5  6  7  8  9
#   10 11 12 13 14
#   15 16 17 18 19
#   20 21 22 23 24

# Neighboring cells of any cell of the board:
NEIGHBORS = ((1, 5, 6),
             (0, 2, 5, 6, 7),
             (1, 3, 6, 7, 8),
             (2, 4, 7, 8, 9),
             (3, 8, 9),
             (0, 1, 6, 10, 11),
             (0, 1, 2, 5, 7, 10, 11, 12),
             (1, 2, 3, 6, 8, 11, 12, 13),
             (2, 3, 4, 7, 9, 12, 13, 14),
             (3, 4, 8, 13, 14),
             (5, 6, 11, 15, 16),
             (5, 6, 7, 10, 12, 15, 16, 17),
             (6, 7, 8, 11, 13, 16, 17, 18),
             (7, 8, 9, 12, 14, 17, 18, 19),
             (8, 9, 13, 18, 19),
             (10, 11, 16, 20, 21),
             (10, 11, 12, 15, 17, 20, 21, 22),
             (11, 12, 13, 16, 18, 21, 22, 23),
             (12, 13, 14, 17, 19, 22, 23, 24),
             (13, 14, 18, 23, 24),
             (15, 16, 21),
             (15, 16, 17, 20, 22),
             (16, 17, 18, 21, 23),
             (17, 18, 19, 22, 24),
             (18, 19, 23))

# Squares that include a given cell:
SQUARES = (((0, 1, 5, 6), (0, 2, 10, 12), (0, 3, 15, 18), (0, 4, 20, 24)),
           ((0, 1, 5, 6),  (1, 2, 6, 7),  (1, 3, 11, 13), (1, 4, 16, 19), (1, 5, 7, 11), (1, 8, 10, 17), (1, 9, 15, 23)),
           ((0, 2, 10, 12), (1, 2, 6, 7), (2, 3, 7, 8), (2, 4, 12, 14), (2, 5, 13, 16), (2, 6, 8, 12), (2, 9, 11, 18), (2, 10, 14, 22)),
           ((0, 3, 15, 18), (1, 3, 11, 13), (2, 3, 7, 8), (3, 4, 8, 9), (3, 5, 19, 21), (3, 6, 14, 17), (3, 7, 9, 13)),
           ((0, 4, 20, 24), (1, 4, 16, 19), (2, 4, 12, 14), (3, 4, 8, 9)),
           ((0, 1, 5, 6), (1, 5, 7, 11), (2, 5, 13, 16), (3, 5, 19, 21), (5, 6, 10, 11), (5, 7, 15, 17), (5, 8, 20, 23)),
           ((0, 1, 5, 6), (1, 2, 6, 7), (2, 6, 8, 12), (3, 6, 14, 17), (5, 6, 10, 11), (6, 7, 11, 12), (6, 8, 16, 18), (6, 9, 21, 24), (6, 10, 12, 16), (6, 13, 15, 22)),
           ((1, 2, 6, 7), (1, 5, 7, 11), (2, 3, 7, 8), (3, 7, 9, 13), (5, 7, 15, 17), (6, 7, 11, 12), (7, 8, 12, 13), (7, 9, 17, 19), (7, 10, 18, 21), (7, 11, 13, 17), (7, 14, 16, 23)),
           ((1, 8, 10, 17), (2, 3, 7, 8), (2, 6, 8, 12), (3, 4, 8, 9), (5, 8, 20, 23), (6, 8, 16, 18), (7, 8, 12, 13), (8, 9, 13, 14), (8, 11, 19, 22), (8, 12, 14, 18)),
           ((1, 9, 15, 23), (2, 9, 11, 18), (3, 4, 8, 9), (3, 7, 9, 13), (6, 9, 21, 24), (7, 9, 17, 19), (8, 9, 13, 14)),
           ((0, 2, 10, 12), (1, 8, 10, 17), (2, 10, 14, 22), (5, 6, 10, 11), (6, 10, 12, 16), (7, 10, 18, 21), (10, 11, 15, 16), (10, 12, 20, 22)),
           ((1, 3, 11, 13), (1, 5, 7, 11), (2, 9, 11, 18), (5, 6, 10, 11), (6, 7, 11, 12), (7, 11, 13, 17), (8, 11, 19, 22), (10, 11, 15, 16), (11, 12, 16, 17), (11, 13, 21, 23), (11, 15, 17, 21)),
           ((0, 2, 10, 12), (2, 4, 12, 14), (2, 6, 8, 12), (6, 7, 11, 12), (6, 10, 12, 16), (7, 8, 12, 13), (8, 12, 14, 18), (10, 12, 20, 22), (11, 12, 16, 17), (12, 13, 17, 18), (12, 14, 22, 24), (12, 16, 18, 22)),
           ((1, 3, 11, 13), (2, 5, 13, 16), (3, 7, 9, 13), (6, 13, 15, 22), (7, 8, 12, 13), (7, 11, 13, 17), (8, 9, 13, 14), (11, 13, 21, 23), (12, 13, 17, 18), (13, 14, 18, 19), (13, 17, 19, 23)),
           ((2, 4, 12, 14), (2, 10, 14, 22), (3, 6, 14, 17), (7, 14, 16, 23), (8, 9, 13, 14), (8, 12, 14, 18), (12, 14, 22, 24), (13, 14, 18, 19)),
           ((0, 3, 15, 18), (1, 9, 15, 23), (5, 7, 15, 17), (6, 13, 15, 22), (10, 11, 15, 16), (11, 15, 17, 21), (15, 16, 20, 21)),
           ((1, 4, 16, 19), (2, 5, 13, 16), (6, 8, 16, 18), (6, 10, 12, 16), (7, 14, 16, 23), (10, 11, 15, 16), (11, 12, 16, 17), (12, 16, 18, 22), (15, 16, 20, 21), (16, 17, 21, 22)),
           ((1, 8, 10, 17), (3, 6, 14, 17), (5, 7, 15, 17), (7, 9, 17, 19), (7, 11, 13, 17), (11, 12, 16, 17), (11, 15, 17, 21), (12, 13, 17, 18), (13, 17, 19, 23), (16, 17, 21, 22), (17, 18, 22, 23)),
           ((0, 3, 15, 18), (2, 9, 11, 18), (6, 8, 16, 18), (7, 10, 18, 21), (8, 12, 14, 18), (12, 13, 17, 18), (12, 16, 18, 22), (13, 14, 18, 19), (17, 18, 22, 23), (18, 19, 23, 24)),
           ((1, 4, 16, 19), (3, 5, 19, 21), (7, 9, 17, 19), (8, 11, 19, 22), (13, 14, 18, 19), (13, 17, 19, 23), (18, 19, 23, 24)),
           ((0, 4, 20, 24), (5, 8, 20, 23), (10, 12, 20, 22), (15, 16, 20, 21)),
           ((3, 5, 19, 21), (6, 9, 21, 24), (7, 10, 18, 21), (11, 13, 21, 23), (11, 15, 17, 21), (15, 16, 20, 21), (16, 17, 21, 22)),
           ((2, 10, 14, 22), (6, 13, 15, 22), (8, 11, 19, 22), (10, 12, 20, 22), (12, 14, 22, 24), (12, 16, 18, 22), (16, 17, 21, 22), (17, 18, 22, 23)),
           ((1, 9, 15, 23), (5, 8, 20, 23), (7, 14, 16, 23), (11, 13, 21, 23), (13, 17, 19, 23), (17, 18, 22, 23), (18, 19, 23, 24)),
           ((0, 4, 20, 24), (6, 9, 21, 24), (12, 14, 22, 24), (18, 19, 23, 24)))

# The eight symmetries of the 5x5 square:
SYMMETRY = ((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24),
            (4,3,2,1,0,9,8,7,6,5,14,13,12,11,10,19,18,17,16,15,24,23,22,21,20),
            (4,9,14,19,24,3,8,13,18,23,2,7,12,17,22,1,6,11,16,21,0,5,10,15,20),
            (24,19,14,9,4,23,18,13,8,3,22,17,12,7,2,21,16,11,6,1,20,15,10,5,0),
            (24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0),
            (20,21,22,23,24,15,16,17,18,19,10,11,12,13,14,5,6,7,8,9,0,1,2,3,4),
            (20,15,10,5,0,21,16,11,6,1,22,17,12,7,2,23,18,13,8,3,24,19,14,9,4),
            (0,5,10,15,20,1,6,11,16,21,2,7,12,17,22,3,8,13,18,23,4,9,14,19,24))

# Chooses a representant of this position among the 8 possible symmetries:
def representant(N, P):
    return min( (tuple(sorted(s[n] for n in N)),
                 tuple(sorted(s[p] for p in P))) for s in SYMMETRY)

# Draws the board:
def board(N, P, caption="\n", NN=None, PP=None):
    if NN is None or PP is None:
        b = ["."] * 25
        for cell in N: b[cell] = "N"
        for cell in P: b[cell] = "P"
        return "\n".join(" ".join(b[i:i+5]) for i in range(0,25,5))+"\n"+caption
    else:
        b1 = ["."] * 25
        b2 = ["."] * 25
        for cell in N:  b1[cell] = "X"
        for cell in P:  b1[cell] = "O"
        for cell in NN: b2[cell] = "X"
        for cell in PP: b2[cell] = "O"
        return "\n".join(" ".join(b1[i:i+5]) + " "*9 + " ".join(b2[i:i+5])
                         for i in range(0,25,5))+"\n"+caption

# Checks if the board positions is "symmetrical"
def is_symmetrical(N,P):
    return (any(tuple(sorted(s[n] for n in N)) == P for s in SYMMETRY[1:]) and
            any(tuple(sorted(s[n] for n in N)) == N for s in SYMMETRY[1:]))

# Finds all winning moves (given the set of losing positions):
def solutions(N,P, P_WINS):

    # If it is ilegal or it is and endgame, there are no moves:
    if (N in SQUARES[N[0]]) or (P in SQUARES[P[0]]): return tuple()

    # Otherwise, find all legal moves:
    m = []
    for cell in NEIGHBORS[N[0]]:
        if cell not in N and cell not in P:
            candidate = (P, tuple(sorted([N[1],N[2],N[3],cell])))
            if representant(*candidate) in P_WINS: m.append(candidate)
    for cell in NEIGHBORS[N[1]]:
        if cell not in N and cell not in P:
            candidate = (P, tuple(sorted([N[0],N[2],N[3],cell])))
            if representant(*candidate) in P_WINS: m.append(candidate)
    for cell in NEIGHBORS[N[2]]:
        if cell not in N and cell not in P:
            candidate = (P, tuple(sorted([N[0],N[1],N[3],cell])))
            if representant(*candidate) in P_WINS: m.append(candidate)
    for cell in NEIGHBORS[N[3]]:
        if cell not in N and cell not in P:
            candidate = (P, tuple(sorted([N[0],N[1],N[2],cell])))
            if representant(*candidate) in P_WINS: m.append(candidate)
    return tuple(m)


### GAME LOGIC #################################################################

# Legal moves from a given position:
def moves(N, P):

    # If it is ilegal or it is and endgame, there are no moves:
    if (N in SQUARES[N[0]]) or (P in SQUARES[P[0]]): return tuple()

    # Otherwise, find all legal moves:
    m = set()
    for cell in NEIGHBORS[N[0]]:
        if cell not in N and cell not in P:
            m.add(representant(P, (N[1],N[2],N[3],cell)))
    for cell in NEIGHBORS[N[1]]:
        if cell not in N and cell not in P:
            m.add(representant(P, (N[0],N[2],N[3],cell)))
    for cell in NEIGHBORS[N[2]]:
        if cell not in N and cell not in P:
            m.add(representant(P, (N[0],N[1],N[3],cell)))
    for cell in NEIGHBORS[N[3]]:
        if cell not in N and cell not in P:
            m.add(representant(P, (N[0],N[1],N[2],cell)))
    return tuple(m)

# Positions that can reach the given position thorugh a legal move:
def parents(N, P):

    # If it is illegal, there are no parents:
    if N in SQUARES[N[0]]: return tuple()

    # Otherwise, find all legal parents:
    p = set()
    for cell in NEIGHBORS[P[0]]:
        if cell not in N and cell not in P:
            new = representant((P[1],P[2],P[3],cell), N)
            if new[0] not in SQUARES[new[0][0]]: p.add(new)
    for cell in NEIGHBORS[P[1]]:
        if cell not in N and cell not in P:
            new = representant((P[0],P[2],P[3],cell), N)
            if new[0] not in SQUARES[new[0][0]]: p.add(new)
    for cell in NEIGHBORS[P[2]]:
        if cell not in N and cell not in P:
            new = representant((P[0],P[1],P[3],cell), N)
            if new[0] not in SQUARES[new[0][0]]: p.add(new)
    for cell in NEIGHBORS[P[3]]:
        if cell not in N and cell not in P:
            new = representant((P[0],P[1],P[2],cell), N)
            if new[0] not in SQUARES[new[0][0]]: p.add(new)
    return tuple(p)


### MAIN FUNCTION ##############################################################

if __name__ == "__main__":

    print("READING") ###########################################################

    N_WINS = set()
    P_WINS = set()
    DRAWS  = set()
    DEPTH  = dict()

    with open("MONDRAGO_DATABASE.py", 'r') as f:
        for n,line in enumerate(f.readlines()):
            if not n & 1048575: print("    {:7d}/9432071".format(n))
            if line.startswith(" (("):
                i = line.index(':')
                j = line.rindex(',')
                key   = eval(line[1:i])
                value = int(line[i+1:j])
                DEPTH[key] = value
                if   value < 0: DRAWS.add(key)      # Negative depth <=> DRAW
                elif value & 1: N_WINS.add(key)     # Odd depth      <=> N_WINS
                else:           P_WINS.add(key)     # Even depth     <=> P_WINS

    max_depth = max(DEPTH.values())
    min_depth = min(DEPTH.values())


    print("INITIAL POSITIONS") #################################################

    with open("MONDRAGO_INITIAL_POSITIONS.txt", "w") as f:
        f.write("\nCURRENT INITIAL POSITION:\n\n")
        N,P = representant((0,1,23,24),(3,4,20,21))
        d = DEPTH[N,P]
        M = moves(N,P)
        W = sum(m in P_WINS for m in M)
        L = sum(m in N_WINS for m in M)
        D = sum(m in DRAWS  for m in M)
        if   (N,P) in DRAWS:  O = tuple(m for m in M if m in DRAWS)
        elif (N,P) in P_WINS: O = tuple(m for m in M if DEPTH[m] == d-1)
        else: O = tuple(m for m in M if m in P_WINS and DEPTH[m] == d-1)
        info = {'d': d, 'W': W, 'D': D, 'L': L, 'O': len(O)}
        f.write(board(N,P, "\n"+str(info)+"\n\n\n"))

        f.write("\nDRAW INITIAL POSITIONS:\n\n")
        for (N,P) in DRAWS:
            if is_symmetrical(N,P):
                d = DEPTH[N,P]
                M = moves(N,P)
                W = sum(m in P_WINS for m in M)
                L = sum(m in N_WINS for m in M)
                D = sum(m in DRAWS  for m in M)
                O = tuple(m for m in M if m in DRAWS)
                info = {'d': d, 'W': W, 'D': D, 'L': L, 'O': len(O)}
                f.write(board(N,P, "\n"+str(info)+"\n\n\n"))

        f.write("\nN_WINS INITIAL POSITIONS:\n\n")
        for (N,P) in N_WINS:
            if is_symmetrical(N,P):
                d = DEPTH[N,P]
                M = moves(N,P)
                W = sum(m in P_WINS for m in M)
                L = sum(m in N_WINS for m in M)
                D = sum(m in DRAWS  for m in M)
                O = tuple(m for m in M if m in P_WINS and DEPTH[m] == d-1)
                info = {'d': d, 'W': W, 'D': D, 'L': L, 'O': len(O)}
                f.write(board(N,P, "\n"+str(info)+"\n\n\n"))

        f.write("\n(There are no P_WINS initial positions)\n")


    print("SAFEST DRAWS") ######################################################

    with open("MONDRAGO_SAFEST_DRAWS.txt", "w") as f:
        for (N,P) in DRAWS:
            if DEPTH[N,P] == min_depth:
                d = DEPTH[N,P]
                M = moves(N,P)
                W = sum(m in P_WINS for m in M)
                L = sum(m in N_WINS for m in M)
                D = sum(m in DRAWS  for m in M)
                O = tuple(m for m in M if m in DRAWS)
                info = {'d': d, 'W': W, 'D': D, 'L': L, 'O': len(O)}
                f.write(board(N,P, "\n"+str(info)+"\n\n\n"))


    print("DEEPEST POSITIONS") #################################################

    with open("MONDRAGO_DEEPEST_POSITIONS.txt", "w") as f:
        assert(max_depth & 1)
        for (N,P) in N_WINS:
            if DEPTH[N,P] == max_depth:
                d = DEPTH[N,P]
                M = moves(N,P)
                W = sum(m in P_WINS for m in M)
                L = sum(m in N_WINS for m in M)
                D = sum(m in DRAWS  for m in M)
                O = solutions(N,P, P_WINS)
                info = {'d': d, 'W': W, 'D': D, 'L': L}
                for o in O[1:]: f.write(board(N,P, "\n", o[1],o[0]))
                f.write(board(N,P, "\n"+str(info)+"\n\n\n", O[0][1],O[0][0]))


    print("PUZZLES ") ###########################################################

    name = {3:"EASY", 5:"NORMAL", 7:"DIFFICULT", 9:"VERY_DIFFICULT"}
    for target in name.keys():
        print("    Depth {}".format(target))
        with open("MONDRAGO_PUZZLES_{}.txt".format(name[target]), "w") as f:
            for (N,P) in N_WINS:
                d = DEPTH[N,P]
                M = moves(N,P)
                W = sum(m in P_WINS for m in M)
                L = sum(m in N_WINS for m in M)
                D = sum(m in DRAWS  for m in M)
                if (d == target and W == 1 and D == 0 and L > 18 and
                    min(DEPTH[m] for m in M if m in N_WINS) > 1):
                    PP,NN = solutions(N,P, P_WINS)[0]
                    info  = "X plays and wins in {} plies".format(d)
                    info += " (1 winning move, 0 draws)"
                    f.write(board(N,P, "\n"+str(info)+"\n\n\n", NN,PP))
                    print(board(N,P, "\n"+str(info)+"\n\n", NN,PP))

################################################################################
