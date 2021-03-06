
# coding: utf-8

# In[1]:


"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


# In[2]:


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


# In[3]:


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


# In[4]:


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


# In[79]:


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    # Ideas: Adaptive agresiveness for weighted evaluation function    
    blank_spaces_propotion = len(game.get_blank_spaces()) / len(game._board_state)
    aggresiveness = 8 / blank_spaces_propotion
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - aggresiveness * opp_moves)


# In[6]:


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


# In[43]:


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)            

        except SearchTimeout:
            legal_moves = game.get_legal_moves()
            if not legal_moves:
                return best_move
            return legal_moves[0]
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        
        assert(depth > 0)
        
        return max(legal_moves, 
                   key=lambda m: self.min_value(game.forecast_move(m), depth - 1))
    
    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # available moves for opponent player 
        legal_moves = game.get_legal_moves()
        # our player wins
        if not legal_moves:
            return float("inf")
        
        # return score from the point of view of our player
        if depth == 0:
            return self.score(game, self)
        
        return min((self.max_value(game.forecast_move(m), depth-1)                     for m in legal_moves))
    
    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # available moves for our player
        legal_moves = game.get_legal_moves()
        # our player loses
        if not legal_moves:
            return float("-inf")
            
        # return score from the point of view of the our player
        if depth == 0:
            return self.score(game, self)
        
        return max((self.min_value(game.forecast_move(m), depth-1)                     for m in legal_moves))


# In[72]:


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            self.search_depth = 1
            while True:
                best_move = self.alphabeta(game, self.search_depth)
                self.search_depth += 1

        except SearchTimeout:
            return best_move
#             legal_moves = game.get_legal_moves()
#             if not legal_moves:
#                 return best_move
#             return legal_moves[0]
            # pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        # print(self.time_left(), self.TIMER_THRESHOLD)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        
        assert(depth > 0)
        
        m = self.max_value(game, depth, float("-inf"), float("inf"), get_move=True)
        return m

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # available moves for opponent player 
        legal_moves = game.get_legal_moves()
        # our player wins
        if not legal_moves:
            return float("inf")
        
        # return score from the point of view of our player
        if depth == 0:
            return self.score(game, self)
        
        v = float("inf")
        for m in legal_moves:
            v = min(v, self.max_value(game.forecast_move(m), depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        
        return v
    
    def max_value(self, game, depth, alpha, beta, get_move=False):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # available moves for our player
        legal_moves = game.get_legal_moves()
        # our player loses
        if not legal_moves:
            return (-1, -1) if get_move else float("-inf")
        
        # return score from the point of view of the our player
        if depth == 0:
            return self.score(game, self)
        
        max_v = float("-inf")
        best_move = (-1, -1)
        for m in legal_moves:
            v = self.min_value(game.forecast_move(m), depth - 1, alpha, beta)
            if v > max_v:
                best_move = m
                max_v = v
            if max_v >= beta:
                return best_move if get_move else max_v
            alpha = max(alpha, max_v)
        
        if not get_move:
            return max_v
        else:
            return best_move


# ### Example

# In[73]:


def print_moves_info(player, game, depth):
    values = {}
    legal_moves = game.get_legal_moves()
    for m in legal_moves:
        values[m] = player.min_value(game.forecast_move(m), depth - 1)
    for move, value in values.items():
        print('|', ' ' * (8 - depth * 2), move, value)
    return max(values.keys(), key=lambda move: values[move])


# In[80]:


# from isolation import Board
# player1 = AlphaBetaPlayer(search_depth=1, score_fn=custom_score_3)
# player2 = AlphaBetaPlayer(search_depth=1)
# game = Board(player1, player2, width=9, height=9)
# game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 41]
# # game.apply_move((1, 2))
# # game.apply_move((1, 0))
# print(game.to_string())


# In[81]:


# game.apply_move(player1.get_move(game, lambda: 1000))
# print(game.to_string())


# In[15]:


# from isolation import Board
# from sample_players import RandomPlayer
# from sample_players import GreedyPlayer

# # create an isolation board (by default 7x7)
# player1 = RandomPlayer()
# # player1 = RandomPlayer()
# player2 = MinimaxPlayer()
# game = Board(player1, player2)

# # place player 1 on the board at row 2, column 3, then place player 2 on
# # the board at row 0, column 5; display the resulting board state.  Note
# # that the .apply_move() method changes the calling object in-place.
# game.apply_move((2, 3))
# game.apply_move((0, 5))
# # print(game.to_string())

# # players take turns moving on the board, so player1 should be next to move
# assert(player1 == game.active_player)

# # get a list of the legal moves available to the active player
# # print(game.get_legal_moves())

# # get a successor of the current state by making a copy of the board and
# # applying a move. Notice that this does NOT change the calling object
# # (unlike .apply_move()).
# new_game = game.forecast_move((1, 1))
# assert(new_game.to_string() != game.to_string())
# # print("\nOld state:\n{}".format(game.to_string()))
# # print("\nNew state:\n{}".format(new_game.to_string()))

# # play the remainder of the game automatically -- outcome can be "illegal
# # move", "timeout", or "forfeit"
# winner, history, outcome = game.play()
# print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
# print(game.to_string())
# print("Move history:\n{!s}".format(history))


# In[ ]:




