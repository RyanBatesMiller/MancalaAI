import copy
# Mancala AI using Minimax with Alpha-Beta Pruning

# ---------------------------
# STATE FUNCTIONS
# ---------------------------
def SUM(state):
    return sum(state["p1_pits"]) + state["p1_ez"] + sum(state["p2_pits"]) + state["p2_ez"]

def INITIAL_STATE():
        return { 
            "p1_pits": [4, 4, 4, 4, 4, 4], 
            "p2_pits": [4, 4, 4, 4, 4, 4],
            "p1_ez": 0,
            "p2_ez": 0, 
            "turn": True  # True for Player 1, False for Player 2
        }      

def CHANGE_TURN(state):
    state["turn"] = not state["turn"]

def IS_PLAYER1_TURN(state):
    return state["turn"]

def PLAYER1_ENDZONE(state):
    return state["p1_ez"]

def PLAYER2_ENDZONE(state):
    return state["p2_ez"]

def PLAYER1_PITS(state):
    return state["p1_pits"]

def PLAYER2_PITS(state):
    return state["p2_pits"]

def ADD_TO_ENDZONE(state, seeds):
    """Add seeds to the endzone of the current player."""
    if IS_PLAYER1_TURN(state):
        state["p1_ez"] += seeds
    else:
        state["p2_ez"] += seeds

# Game ends when all pits of one player are empty
def TERMINAL_STATE(state):
    return all(pit == 0 for pit in PLAYER1_PITS(state)) or all(pit == 0 for pit in PLAYER2_PITS(state))

def COUNT_SEEDS(state, player):
    """Count total seeds for a player."""
    if player:
        return sum(PLAYER1_PITS(state)) + PLAYER1_ENDZONE(state)
    else:
        return sum(PLAYER2_PITS(state)) + PLAYER2_ENDZONE(state)

# Win when one player's endzone score is greater than the other's at the end of the game
def WINNING_STATE(state, player):
    return TERMINAL_STATE(state) and COUNT_SEEDS(state, player) > COUNT_SEEDS(state, not player)

# Draw if both players have the same score in their endzones at the end of the game
def DRAW_STATE(state):
    return TERMINAL_STATE(state) and COUNT_SEEDS(state, True) == COUNT_SEEDS(state, False)

# Losing state if a player has fewer points in their endzone than the other player at the end of the game
def LOSING_STATE(state, player):
    return TERMINAL_STATE(state) and COUNT_SEEDS(state, player) < COUNT_SEEDS(state, not player)

def GET_PIT(state, player_side, pit_index):
    """Get the value of a pit for a player."""
    if player_side:
        return state["p1_pits"][pit_index]
    else:
        return state["p2_pits"][pit_index]

def SET_PIT(state, player_side, pit_index, value):
    """Set the value of a pit for a player."""
    if player_side:
        state["p1_pits"][pit_index] = value
    else:
        state["p2_pits"][pit_index] = value

# ---------------------------
# SUCCESSOR & ACTIONS
# ---------------------------
def NEXT_STATE(state, selected_pit_index):
    """Compute possible next state for a move, fixing pit-indexing."""
    next_state = copy.deepcopy(state)
    player = IS_PLAYER1_TURN(next_state)
    seeds = GET_PIT(next_state, player, selected_pit_index)
    if seeds == 0:
        return None
    # pick up all seeds
    SET_PIT(next_state, player, selected_pit_index, 0)

    current_side = player
    idx = selected_pit_index
    # distribute seeds one by one
    while seeds > 0:
        idx += 1

        if idx < 6:
            SET_PIT(next_state, current_side, idx, GET_PIT(next_state, current_side, idx) + 1)
            seeds -= 1
        else:
            # place in endzone if own side, else skip
            if current_side == player:
                ADD_TO_ENDZONE(next_state, 1)
                seeds -= 1
            idx = -1
            current_side = not current_side

    # idx == -1 means last seed in endzone
    # capture rule: if last seed landed in an empty pit on player's side
    if current_side == player and idx >= 0 and GET_PIT(next_state, player, idx) == 1:
        opp_idx = 5 - idx
        captured = GET_PIT(next_state, not player, opp_idx)
        ADD_TO_ENDZONE(next_state, captured + 1)
        SET_PIT(next_state, not player, opp_idx, 0)
        # remove the landing seed
        SET_PIT(next_state, player, idx, 0)
        CHANGE_TURN(next_state)

    elif not (idx == -1 and not current_side == player):
        # if last seed did not land in player's endzone, change turn
        CHANGE_TURN(next_state)
    return next_state


def SUCC_FN(state):
    """Generate all legal successors from current state."""
    successors = []
    for pit_index in range(6):
        nxt = NEXT_STATE(state, pit_index)
        if nxt is not None:
            successors.append(nxt)
    return successors

# ---------------------------
# EVALUATION & SEARCH
# ---------------------------
def EVAL(state, player):
    """Evaluate the state for the current player."""
    if WINNING_STATE(state, player):
        return 1000  # Winning state
    if LOSING_STATE(state, player):
        return -1000  # Losing state
    if DRAW_STATE(state):
        return 0  # Draw state
    # Simple heuristic: endzone difference + turn bonus
    diff = COUNT_SEEDS(state, player) - COUNT_SEEDS(state, not player)
    bonus = 10 if IS_PLAYER1_TURN(state) == player else 0
    return diff + bonus


def MINIMAX_ALPHA_BETA(state, depth, is_maximizing, alpha, beta, player):
    # Terminal or depth 0
    if depth == 0 or TERMINAL_STATE(state):
        return EVAL(state, player), None

    best_move = None
    if is_maximizing:
        value = float('-inf')
        for i in range(6):
            child = NEXT_STATE(state, i)
            if child:
                eval_child, _ = MINIMAX_ALPHA_BETA(child, depth-1, child['turn']==player, alpha, beta, player)
                if eval_child > value:
                    value, best_move = eval_child, i
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return value, best_move
    else:
        value = float('inf')
        for i in range(6):
            child = NEXT_STATE(state, i)
            if child:
                eval_child, _ = MINIMAX_ALPHA_BETA(child, depth-1, child['turn']==player, alpha, beta, player)
                if eval_child < value:
                    value, best_move = eval_child, i
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return value, best_move

# ---------------------------
# GAME CLASS
# ---------------------------
class GAME:
    def __init__(self, depth=8):
        self.state = INITIAL_STATE()
        self.depth = depth

    def SET_STATE(self, new_state):
        self.state = new_state

    def GET_STATE(self):
        return self.state
    
    def UPDATE_DEPTH(self, new_depth):
        self.depth = new_depth
    
    def PRINT_BOARD(self):
        print("\n      ", end="")
        print(" ".join(f"[{i}]" for i in range(6, 0, -1)))  # Pit indices P2

        print(" P2  ", end="")
        print(" ".join(f"[{p}]" for p in PLAYER2_PITS(self.state)[::-1]))
        print(f"[{PLAYER2_ENDZONE(self.state)}]" + " "*25 + f"[{PLAYER1_ENDZONE(self.state)}]")

        print(" P1  ", end="")
        print(" ".join(f"[{p}]" for p in PLAYER1_PITS(self.state)))
        print("      ", end="")
        print(" ".join(f"[{i}]" for i in range(1, 7)))  # Pit indices P1
        print()


    def PLAY_INTERACTIVE(self):
        while not TERMINAL_STATE(self.state):
            # display board
            self.PRINT_BOARD()
            if IS_PLAYER1_TURN(self.state):
                move = None
                while move is None:
                    choice = input("Your move (1-6): ")
                    if choice.isdigit() and 1 <= int(choice) <= 6 and GET_PIT(self.state, True, int(choice)-1)>0:
                        move = int(choice)-1
                    else:
                        print("Invalid. Choose a non-empty pit 1-6.")
                self.SET_STATE(NEXT_STATE(self.state, move))
            else:
                print("AI thinking...")
                _, ai_move = MINIMAX_ALPHA_BETA(self.state, self.depth, True, float('-inf'), float('inf'), False)
                print(f"AI picks pit {ai_move+1}")
                self.SET_STATE(NEXT_STATE(self.state, ai_move))
        # game over
        self.PRINT_BOARD()
        print("Game over!")
        print("Final -> YOU:", COUNT_SEEDS(self.state, True), "AI:", COUNT_SEEDS(self.state, False))

    def PLAY_SELF(self):
        while not TERMINAL_STATE(self.state):
            self.PRINT_BOARD()
            player = IS_PLAYER1_TURN(self.state)
            _, move = MINIMAX_ALPHA_BETA(self.state, self.depth, True, float('-inf'), float('inf'), player)
            print(f"Player {'1' if player else '2'} moves pit {move+1}")
            self.SET_STATE(NEXT_STATE(self.state, move))
        self.PRINT_BOARD()
        print("Game over!")
        print("Final -> P1:", COUNT_SEEDS(self.state, True), "P2:", COUNT_SEEDS(self.state, False))


def main():

    while (True):
        mode = input("Enter 'self' or 'play': ")
        game = GAME()
        depth = input("Depth for AI (default 8): ")
        game.UPDATE_DEPTH(int(depth) if depth.isdigit() else 8)
        if mode=='self':
            game.PLAY_SELF()
        elif mode=='play':
            game.PLAY_INTERACTIVE()
        else:
            print("Invalid mode. Please enter 'self' or 'play'.")

if __name__ == "__main__":
    main()
