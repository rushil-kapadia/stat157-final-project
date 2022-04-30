import chess.pgn
from stockfish import Stockfish
import random

def question_gen():
    game_file = open("data/lichess_db_standard_rated_2013-01.pgn", "r")
    game_txts = game_file.read()
    game_split_txt = game_txts.split("\n\n")
    filtered_split_text = [(game_split_txt[i],game_split_txt[i+1]) for i in range(0,int(len(game_split_txt)), 2) if "Classical" in game_split_txt[i] and len(game_split_txt[i+1].split()) > 60]
    game_selected = random.choice(filtered_split_text)
    game_txt = game_selected[0] + "\n\n" + game_selected[1]

    with open("data/tmp.pgn", "w") as tmp:
        tmp.write(game_txt)
    with open("data/tmp.pgn", "r") as tmp:
        game = chess.pgn.read_game(tmp)
    board = game.board()

    question_num_moves = 30
    count = 0
    for move in game.mainline_moves():
        board.push(move)
        if count > question_num_moves:
            break
        count += 1
    with open("data/game.svg", "w") as f:
        f.write(chess.svg.board(board))

    fen = board.fen()
    stockfish = Stockfish(path="/usr/local/Cellar/stockfish/15/bin/stockfish",depth=20)
    stockfish.set_fen_position(fen)
    eval = stockfish.get_evaluation()
    if eval["type"] == 'mate':
        return question_gen()
        
    return eval["value"], fen
