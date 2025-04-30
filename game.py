from random import randrange

def generate_html_board(board):
    """Generate HTML representation of the board"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tic Tac Toe</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }
            .board {
                display: grid;
                grid-template-columns: repeat(3, 100px);
                grid-template-rows: repeat(3, 100px);
                gap: 5px;
                margin: 20px 0;
            }
            .cell {
                background-color: white;
                border: 2px solid #333;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                font-weight: bold;
                cursor: pointer;
            }
            .cell.X { color: #ff4757; }
            .cell.O { color: #2ed573; }
            .message {
                font-size: 1.5rem;
                margin: 20px 0;
                font-weight: bold;
            }
            .controls {
                margin-top: 20px;
            }
            input, button {
                padding: 8px 12px;
                font-size: 1rem;
            }
        </style>
    </head>
    <body>
        <h1>Tic Tac Toe</h1>
        <div class="board">
    """
    
    for row in range(3):
        for col in range(3):
            value = board[row][col]
            cell_class = "X" if value == "X" else "O" if value == "O" else ""
            html += f'<div class="cell {cell_class}">{value}</div>'
    
    html += """
        </div>
        <div class="message">Enter your move (1-9)</div>
        <div class="controls">
            <form method="post">
                <input type="number" name="move" min="1" max="9" required>
                <button type="submit">Submit Move</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html

def display_board(board):
    """Display the board in console and generate HTML"""
    # Console output
    print("+-------" * 3, "+", sep="")
    for row in range(3):
        print("|       " * 3, "|", sep="")
        for col in range(3):
            print("|   " + str(board[row][col]) + "   ", end="")
        print("|")
        print("|       " * 3, "|", sep="")
        print("+-------" * 3, "+", sep="")
    
    # HTML output
    with open("tic_tac_toe.html", "w") as f:
        f.write(generate_html_board(board))

def enter_move(board):
    """Handle the user's move"""
    ok = False
    while not ok:
        move = input("Enter your move (1-9): ")
        ok = len(move) == 1 and move >= '1' and move <= '9'
        if not ok:
            print("Bad move - repeat your input!")
            continue
        move = int(move) - 1
        row = move // 3
        col = move % 3
        sign = board[row][col]
        ok = sign not in ['O', 'X']
        if not ok:
            print("Field already occupied - repeat your input!")
            continue
    board[row][col] = 'O'

def make_list_of_free_fields(board):
    """Return a list of free squares"""
    free = []
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ['O', 'X']:
                free.append((row, col))
    return free

def victory_for(board, sgn):
    """Check if the specified player has won"""
    if sgn == "X":
        who = 'me'
    elif sgn == "O":
        who = 'you'
    else:
        who = None
    
    # Check rows and columns
    for rc in range(3):
        if board[rc][0] == sgn and board[rc][1] == sgn and board[rc][2] == sgn:
            return who
        if board[0][rc] == sgn and board[1][rc] == sgn and board[2][rc] == sgn:
            return who
    
    # Check diagonals
    if board[0][0] == sgn and board[1][1] == sgn and board[2][2] == sgn:
        return who
    if board[2][0] == sgn and board[1][1] == sgn and board[0][2] == sgn:
        return who
    
    return None

def draw_move(board):
    """Computer makes a random move"""
    free = make_list_of_free_fields(board)
    if free:
        this = randrange(len(free))
        row, col = free[this]
        board[row][col] = 'X'

# Initialize the game
board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
board[1][1] = 'X'  # Computer starts in the center
free = make_list_of_free_fields(board)
human_turn = True

# Main game loop
while len(free):
    display_board(board)
    if human_turn:
        enter_move(board)
        victor = victory_for(board, 'O')
    else:
        draw_move(board)
        victor = victory_for(board, 'X')
    
    if victor is not None:
        break
    
    human_turn = not human_turn
    free = make_list_of_free_fields(board)

# Final display and result
display_board(board)
if victor == 'you':
    print("You won!")
elif victor == 'me':
    print("I won!")
else:
    print("Tie!")