
#######################################################################
#                                                                     #
# MONDRAGO SOLVER: A brute force script to solve the game of Mondrago #
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

    N_WINS = set()      # Next Player Wins
    P_WINS = set()      # Previous Player Wins
    DRAWS  = set()      # Draws by repetition
    QUEUE  = set()      # 
    DEPTH  = dict()     # Length of optimal play
    
    ### CLASSIFY ALL POSITIONS #################################################

    print("CLASSIFY")

    from itertools import combinations

    # Generate all legal the positions of the game:
    for N in combinations(range(25), 4):
        if N not in SQUARES[N[0]]:      # N is a square <=> Illegal position
            for P in combinations(tuple(c for c in range(25) if c not in N), 4):
                if P in SQUARES[P[0]]:  # P is a square <=> Endgame position
                    P_WINS.add(representant(N,P))
                else:                   # N,P is a draw until proven otherwise
                    DRAWS.add(representant(N,P))

    # Initialize the QUEUE
    for N,P in P_WINS:
        for parent in parents(N,P):
            if parent in DRAWS:
                QUEUE.add(parent)

    # Keep updating until done:
    while QUEUE:

        N,P = QUEUE.pop()
        M   = moves(N,P)
        
        # If there is a winning move:
        if any(m in P_WINS for m in M):
            N_WINS.add((N,P))
            DRAWS.discard((N,P))
            QUEUE.update(p for p in parents(N,P) if p in DRAWS)
                    
        # If all moves are losing:
        elif all(m in N_WINS for m in M):
            P_WINS.add((N,P))
            DRAWS.discard((N,P))
            QUEUE.update(p for p in parents(N,P) if p in DRAWS)

    ### COMPUTE DEPTHS #########################################################

    print("DEPTHS")

    # Compute the DEPTH of endgame positions
    for N,P in P_WINS:
        if P in SQUARES[P[0]]:
            DEPTH[N,P] = 0
            QUEUE.update(parents(N,P))
                    
    # Keep updating until done:
    while QUEUE:

        LAYER = list(QUEUE)
        QUEUE = set()

        while LAYER:

            N,P = LAYER.pop()
            M   = moves(N,P)
            
            # If there is a winning move:
            if any(m in P_WINS and m in DEPTH for m in M):
                DEPTH[N,P] = 1 + min(DEPTH[m] for m in M if m in P_WINS and m in DEPTH)
                QUEUE.update(p for p in parents(N,P) if p in P_WINS and p not in DEPTH)
                        
            # If all moves are losing:
            elif all(m in N_WINS and m in DEPTH for m in M):
                DEPTH[N,P] = 1 + max(DEPTH[m] for m in M)
                QUEUE.update(p for p in parents(N,P) if p in N_WINS and p not in DEPTH)

    print("DRAWS")

    # The DEPTH of a DRAW is its (negative) minimum distance to a losing move
    count = len(DRAWS)
    for N,P in DRAWS:
        if any(m not in DRAWS for m in moves(N,P)):
            DEPTH[N,P] = -1
            count     -= 1

    # Keep updating until done:
    depth = -1
    while count:
        for N,P in DRAWS:
            if (N,P) not in DEPTH:
                if any(m in DEPTH and DEPTH[m] == depth for m in moves(N,P)):
                    DEPTH[N,P] = depth - 1
                    count     -= 1
        depth -= 1

    ### OUTPUT RESULTS #########################################################

    print("OUTPUT")

    from collections import Counter

    with open("MONDRAGO_STATS.txt", "w") as f:
        f.write("Number of N wins positions: {:7d}\n".format(len(N_WINS)))
        f.write("Number of P wins positions: {:7d}\n".format(len(P_WINS)))
        f.write("Number of drawn  positions: {:7d}\n".format(len(DRAWS)))
        f.write("Number of legal  positions: {:7d}\n".format(len(DEPTH)))
        f.write("\n")
        for depth,size in sorted(Counter(DEPTH.values()).items()):
            f.write("     Positions at depth {:2d}: {:7d}\n".format(depth,size))
        f.write("\n(draws have negative depths)\n")
    
    with open("MONDRAGO_DATABASE.py", "w") as f:
        f.write("# (NextPlayerPieces, NextPlayerPieces): Depth\n")
        f.write("#\n")
        f.write("# Depth: for draws is (negative) minimum distance to a losing position (draw positions that have losing moves have depth -1)\n")
        f.write("#        otherwise is the length of optimal play, assuming that the winning player tries to win fast and the losing plyaer tries to delay the defeat (endgame positions have depth 0)\n")
        f.write("#\n")
        f.write("DEPTH = {\n")
        for (N,P),d in sorted(DEPTH.items()):
            f.write(" ({},{}):{},\n".format(N,P,d))
        f.write("}\n")

    ### SANITY CHECKS ##########################################################

    print("TESTS")
    
    assert(len(N_WINS) + len(P_WINS) + len(DRAWS) == len(DEPTH))
    for N,P in N_WINS:
        assert(any(m in P_WINS for m in moves(N,P)))
        assert(DEPTH[N,P] == 1+min(DEPTH[m] for m in moves(N,P) if m in P_WINS))
    for N,P in P_WINS:
        assert(all(m in N_WINS for m in moves(N,P)))
        assert((P in SQUARES[P[0]] and DEPTH[N,P] == 0) or
               (DEPTH[N,P] == 1+max(DEPTH[m] for m in moves(N,P))))
    for N,P in DRAWS:
        M = moves(N,P)
        O = tuple(m for m in M if m in DRAWS)
        assert(all(m not in P_WINS for m in M) and any(m in DRAWS for m in M))
        assert((len(O) < len(M) and DEPTH[N,P] == -1) or
               (DEPTH[N,P]+1 == max(DEPTH[m] for m in O)))

    print("DONE!")

################################################################################
