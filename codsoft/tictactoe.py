import math

# Initialize the Tic-Tac-Toe board
def initialize_board():
    return [' ' for _ in range(9)]

# Display the board
def display_board(board):
    print("\n")
    for i in range(3):
        print(" | ".join(board[i * 3:(i + 1) * 3]))
        if i < 2:
            print("-" * 5)
    print("\n")

# Check if a player has won
def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

# Check if the game is a draw
def is_draw(board):
    return ' ' not in board

# Get all available moves
def get_available_moves(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

# Minimax algorithm
def minimax(board, depth, is_maximizing, alpha, beta):
    # Base cases
    if check_winner(board, 'O'):  # AI wins
        return 10 - depth
    if check_winner(board, 'X'):  # Human wins
        return depth - 10
    if is_draw(board):  # Draw
        return 0

    # Maximizing player's turn (AI)
    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth + 1, False, alpha, beta)
            board[move] = ' '
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:  # Alpha-Beta Pruning
                break
        return best_score
    else:  # Minimizing player's turn (Human)
        best_score = math.inf
        for move in get_available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth + 1, True, alpha, beta)
            board[move] = ' '
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:  # Alpha-Beta Pruning
                break
        return best_score

# AI makes its move
def ai_move(board):
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        board[move] = 'O'
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

# Main game loop
def tic_tac_toe():
    print("Welcome to Tic-Tac-Toe!")
    board = initialize_board()
    display_board(board)

    # Choose who goes first
    player_turn = input("Do you want to be X (first) or O (second)? ").upper() == 'X'

    while True:
        # Human player's turn
        if player_turn:
            move = -1
            while move not in get_available_moves(board):
                try:
                    move = int(input("Enter your move (0-8): "))
                    if move not in get_available_moves(board):
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 0 and 8.")
            board[move] = 'X'
        else:
            # AI's turn
            print("AI is thinking...")
            move = ai_move(board)
            board[move] = 'O'
        3

        # Display the board
        display_board(board)

        # Check for game end
        if check_winner(board, 'X'):
            print("You win! Congratulations!")
            break
        if check_winner(board, 'O'):
            print("AI wins! Better luck next time.")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch turns
        player_turn = not player_turn

# Run the game
tic_tac_toe()
