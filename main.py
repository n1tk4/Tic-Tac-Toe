import shelve
import json

def start_board():
    board = {
        1 : " ", 2 : " ", 3 : " ",
        4 : " ", 5 : " ", 6 : " ",
        7 : " ", 8 : " ", 9 : " "
    }
    return board


def render(board):
    print('Current board:')
    print('+---+---+---+')
    print(f"| {board[1]} | {board[2]} | {board[3]} |   1  2  3")
    print('+---+---+---+')
    print(f"| {board[4]} | {board[5]} | {board[6]} |   4  5  6")
    print('+---+---+---+')
    print(f"| {board[7]} | {board[8]} | {board[9]} |   7  8  9")
    print('+---+---+---+')


def get_move():
    valid_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    chosen_position = ""
    try:
        chosen_position = input("Give a position move: ")
    except KeyboardInterrupt:
        print("You successfully exited!")
    while chosen_position not in valid_moves:
        try:
            chosen_position = int(chosen_position)
        except ValueError:
            chosen_position = input("Please give a legal position: ")
        if chosen_position in valid_moves:
            break
    return chosen_position


def make_move(board, chosen_position, player):
    while board[chosen_position] != " ":
        print(f"Can't make move {chosen_position}, square already taken!")
        chosen_position = get_move()
    new_board = board
    new_board[chosen_position] = player


def get_winner(board):
    winner = " "

    # Rows
    if board[1] == board[2] == board[3] and board[1] != " ":
        winner = board[1]
    elif board[4] == board[5] == board[6] and board[4] != " ":
        winner = board[4]
    elif board[7] == board[8] == board[9] and board[7] != " ":
        winner = board[7]

    # Columns
    elif board[1] == board[4] == board[7] and board[1] != " ":
        winner = board[1]
    elif board[2] == board[5] == board[8] and board[2] != " ":
        winner = board[2]
    elif board[3] == board[6] == board[9] and board[3] != " ":
        winner = board[3]

    # Diagonals
    elif board[1] == board[5] == board[9] and board[1] != " ":
        winner = board[5]
    elif board[3] == board[5] == board[7] and board[3]!= " ":
        winner = board[5]
    return winner


def checkDraw(board):
    for key in board.keys():
        if board[key] == " ":
            return False
    return True


def compMove(board):
    bestScore = -1000
    bestMove = 0
    for key in board.keys():
        if (board[key] == " "):
            board[key] = "O"
            score = minimax(board, False)
            board[key] = " "
            if (score > bestScore):
                bestScore = score
                bestMove = key
    return bestMove


def minimax(board, isMaximizing):
    if get_winner(board) == 'O':
        return 1     
    elif get_winner(board) == 'X':
        return -1
    elif checkDraw(board):
        return 0
    if isMaximizing:
        bestScore = -99
        for key in board.keys():
            if (board[key] == " "):
                board[key] = "O"
                score = minimax(board, False)
                board[key] = " "
                if (score > bestScore):
                    bestScore = score
        return bestScore
    else:
        bestScore = 99
        for key in board.keys():
            if (board[key] == " "):
                board[key] = "X"
                score = minimax(board, True)
                board[key] = " "
                if (score < bestScore):
                    bestScore = score
        return bestScore

def save(board):
    shelfFile = shelve.open('savedGame')
    shelfFile['board'] = board
    shelfFile.close()


def load():
    shelfFile = shelve.open('savedGame')
    board = shelfFile['board']
    shelfFile.close()
    return board


def whichBoard():
    pass

def saveJson(board):
    filename = 'board.json'
    board = board
    with open(filename, 'w') as f:
        json.dump(board, f)


def play():
    counter = 0
    board = start_board()
    inp = input("Do you want load the previous game? y/n: ")
    if inp == 'y':
        board = load()
    while True:
        render(board)
        save(board)
        saveJson(board)
        if  get_winner(board) != " ":
            print(f"The winner is {get_winner(board)}")
            break
        elif checkDraw(board):
            print("It's a draw")
            break
        if counter % 2 == 0:
            player = "X"
            print(f"Now {player} is turn")
            make_move(board, get_move(), player)
        else:
            player = "O"
            print(f"Now {player} is turn")
            make_move(board, compMove(board), player)
        counter += 1


play()

with open('board.json') as f:
    board = json.load(f)


print(board)
