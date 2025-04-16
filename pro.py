import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import Button
from functools import partial
from PIL import ImageTk, Image 
class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def match(self,list_pos):
        for pos in list_pos:
            if pos.row == self.row and pos.col == self.col:
                return True
        return False
class Piece:
    def __init__(self, color, board, position=None):
        self.color = color
        self.board = board
        self.has_moved = False 
        self.position = position
    def __str__(self):
        pass
class King(Piece):
    def __init__(self,color,board,pic1, pic2,position=None):
        super().__init__(color,board,position)
        self.piece_type = "king"
        self.im1 = pic1
        self.im2 = pic2
        
    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        if not self.board.board[self.position.row][self.position.col].has_moved:
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(self.position.col + 1, 7)):
                    moves.append(Position(self.position.row, self.position.col + 2))
            if  self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves.append(Position(self.position.row, self.position.col - 2))
        return moves
    def move(self,end_pos):
        a = self.possible_moves()
        for pos in a:
            if pos.row == end_pos.row and pos.col == end_pos.col:
                return True
        return False
    def __str__(self):
        if self.color == "White":
            return "K"
        return "k" 
class Bishop(Piece):
    def __init__(self,color,board,pic1,pic2,position=None):
        super().__init__(color,board,position)
        self.piece_type = "bishop"
        self.im1 = pic1
        self.im2 = pic2
    def possible_moves(self):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            temp = self.position
            while True:
                new_pos = Position(temp.row + dr, temp.col + dc)
                temp = new_pos
                if self.board.is_inside_board(new_pos) == False:
                    break
                if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    moves.append(new_pos)
                if self.board.is_enemy_piece(new_pos, self.color):
                    break
                if not self.board.is_square_empty(new_pos):
                    break
        return moves
    def move(self,end_pos):
        a = self.possible_moves()
        for pos in a:
            if pos.row == end_pos.row and pos.col == end_pos.col:
                return True
        return False
    def __str__(self):
        if self.color == "White":
            return "B"
        return "b" 
class Pawn(Piece):
    def __init__(self,color,board,pic1, pic2,position=None):
        super().__init__(color,board,position)
        self.piece_type = "pawn"
        self.im1 = pic1
        self.im2 = pic2
    def possible_moves(self):
        moves = []
        direction = 1 if self.color == "White" else -1
        start_row = 1 if self.color == "White" else 6
        temp = self.position
        count = 0
        if start_row == temp.row:
            help = 2
        else:
            help = 1
        while count < help:
            new_pos = Position(temp.row + direction, temp.col)
            temp = new_pos
            if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos):
                moves.append(new_pos)
            else:
                break
            count += 1
        temp = self.position
        new_pos = Position(temp.row + direction, temp.col - 1)
        if self.board.is_inside_board(new_pos):
            if self.board.is_enemy_piece(new_pos, self.color):
                moves.append(new_pos)
        new_pos = Position(temp.row + direction, temp.col + 1)
        if self.board.is_inside_board(new_pos):
            if self.board.is_enemy_piece(new_pos, self.color):
                moves.append(new_pos)
        if self.board.last_piece_move:
            if self.board.last_piece_move.position.row == temp.row:
                if self.board.last_piece_move.position.col == temp.col + 1:
                    if not self.board.board[self.board.last_piece_move.position.row + direction][temp.col + 1]:
                        if self.board.last_piece_move.piece_type == "pawn":
                            moves.append(Position(self.board.last_piece_move.position.row + direction, temp.col + 1))
                if self.board.last_piece_move.position.col == temp.col - 1:
                    if not self.board.board[self.board.last_piece_move.position.row + direction][temp.col - 1]:
                        if self.board.last_piece_move.piece_type == "pawn":
                            moves.append(Position(self.board.last_piece_move.position.row + direction, temp.col - 1))
        return moves
    def move(self,end_pos):
        a = self.possible_moves()
        for pos in a:
            if pos.row == end_pos.row and pos.col == end_pos.col:
                return True
        return False
    def __str__(self):
        if self.color == "White":
            return "P"
        return "p" 
class Rook(Piece):
    def __init__(self,color,board,pic1, pic2,position=None):
        super().__init__(color,board,position)
        self.piece_type = "rook"
        self.im1 = pic1
        self.im2 = pic2
    def possible_moves(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            temp = self.position
            while True:
                new_pos = Position(temp.row + dr, temp.col + dc)
                temp = new_pos
                if self.board.is_inside_board(new_pos) == False:
                    break
                if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                    moves.append(new_pos)
                if not self.board.is_square_empty(new_pos):
                    break
        return moves
    def move(self,end_pos):
        a = self.possible_moves()
        for pos in a:
            if pos.row == end_pos.row and pos.col == end_pos.col:
                return True
        return False
    def __str__(self):
        if self.color == "White":
            return "R"
        return "r" 

class Knight(Piece):
    def __init__(self,color,board,pic1, pic2,position=None):
        super().__init__(color,board,position)
        self.piece_type = "knight"
        self.im1 = pic1
        self.im2 = pic2
    def possible_moves(self):
        moves = []
        ends = [(-2, 1), (-2, -1), (2, -1), (2, 1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        temp = self.position
        for er, ec in ends:
            new_pos = Position(temp.row + er, temp.col + ec)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        return moves
    def move(self,end_pos):
        a = self.possible_moves()
        for pos in a:
            if pos.row == end_pos.row and pos.col == end_pos.col:
                return True
        return False
    def __str__(self):
        if self.color == "White":
            return "N"
        return "n" 
            
class Queen(Piece):
    def __init__(self,color,board ,pic1, pic2,position=None):
        super().__init__(color,board,position)
        self.piece_type = "queen"
        self.im1 = pic1
        self.im2 = pic2
    def possible_moves(self):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            temp = self.position
            while True:
                new_pos = Position(temp.row + dr, temp.col + dc)
                temp = new_pos
                if self.board.is_inside_board(new_pos):
                    if self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color):
                        moves.append(new_pos)
                if not self.board.is_inside_board(new_pos):
                    break
                if not self.board.is_square_empty(new_pos):
                    break
        return moves
    def move(self,end_pos):
        a = self.possible_moves()
        for pos in a:
            if pos.row == end_pos.row and pos.col == end_pos.col:
                return True
        return False
    def __str__(self):
        if self.color == "White":
            return "Q"
        return "q"
class Board:
    def __init__(self):     
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.left_click = [[0 for _ in range(8)] for _ in range(8)]
        self.right_click = [[0 for _ in range(8)] for _ in range(8)]
        self.current_player = "Black"
        self.cc = 0
        self.last_piece_move = None
        self.pawn_promition = 0
        self.ischecking = False
        self.remiw = 0
        self.remib = 0
        for i in range(8):
            for j in range(8):
                if (i==0 or i==7) and (j==4 or j ==5):
                    bt = Button(master, text = '')
                    bt.bind("<Button-1>", self.inner1(i, j))
                    bt.bind("<Button-2>", self.inner2(i, j))
                    self.buttons[i][j] = bt
                    bt.grid(row = i, column = j)
                else:
                    if ((i + j) % 2 == 0):
                        bt = Button(master, text = '', image = white)
                    else:
                        bt = Button(master, text = '', image = blue)
                    bt.bind("<Button-1>", self.inner1(i, j))
                    bt.bind("<Button-2>", self.inner2(i, j))
                    self.buttons[i][j] = bt
                    bt.grid(row = i, column = j)
    def inner1(self, i, j):
        def lft(l):
            if self.board[i][j]:
                for ii in range(8):
                    for jj in range(8):
                        self.left_click[ii][jj] = 0
                        self.buttons[ii][jj].config(highlightthickness = 1.2,highlightbackground = 'white')
                if self.board[i][j]:
                    if self.board[i][j].color == self.current_player:
                        self.left_click[i][j] = 1
                        self.buttons[i][j].config(highlightthickness = 1.2  ,highlightbackground = "#000000")
                        for x in self.board[i][j].possible_moves():
                            if self.board[x.row][x.col]:
                                self.buttons[x.row][x.col].config(highlightthickness = 1.2  ,highlightbackground = "#ff0000")
                            else:
                                self.buttons[x.row][x.col].config(highlightthickness = 1.2  ,highlightbackground = "#008000")
                    else:
                        self.buttons[i][j].config(highlightthickness = 1.2  ,highlightbackground = "#000000")

                                
        return lft
    def inner2(self, i, j):
        def rgt(l):
            flag = False
            for ii in range(8):
                for jj in range(8):
                    self.buttons[ii][jj].config(highlightthickness = 1.2,highlightbackground = '#fff')
                    if self.left_click[ii][jj] == 1:
                        flag = True
                        co_ii = ii
                        co_jj = jj
            if flag == True:
                for ii in range(8):
                    for jj in range(8):
                        self.right_click[ii][jj] = 0
                self.right_click[i][j] = 1
                if self.board[co_ii][co_jj].move(Position(i, j)):
                    co_1 = self.board[co_ii][co_jj]
                    co_2 = self.board[i][j]
                    hmove1 = None
                    hmove2 = None
                    if co_1:
                        hmove1 = co_1.has_moved
                    if co_2:
                        hmove2 = co_2.has_moved
                    en_passant = 0
                    en_passant_copy = None
                    if co_1.piece_type == "pawn" and co_jj != j:
                        if not co_2:
                            en_passant = 1
                            en_passant_copy = self.board[co_ii][j]
                    if co_1.piece_type != "king" or (co_1.piece_type == "king" and abs(co_jj - j) <= 1) or (co_1.piece_type == "king" and abs(co_jj - j) > 1 and not self.is_check(self.current_player)):
                        self.move_piece(Position(co_ii, co_jj), Position(i, j))
                    if en_passant:
                        pawnbichare = self.board[co_ii][j]
                        self.remove_piece(self.board[co_ii][j])
                    if co_1.piece_type == "king" and (co_ii == i) and (abs(co_jj - j) > 1) and not self.is_check(self.current_player):
                        Hsmove = None
                        if co_1.color == "White":
                            if co_ii == 0:
                                if j > co_jj:
                                    Hsmove = self.board[0][7].has_moved
                                    self.cc = 1
                                    self.move_piece(Position(0, 7), Position(0, 5))
                                if j < co_jj:
                                    Hsmove = self.board[0][0].has_moved
                                    self.cc = 1
                                    self.move_piece(Position(0, 0), Position(0, 3))
                        if co_1.color == "Black":
                            if co_ii == 7:
                                if j > co_jj:
                                    Hsmove = self.board[7][7].has_moved
                                    self.cc = 1
                                    self.move_piece(Position(7, 7), Position(7, 5))
                                if j < co_jj:
                                    Hsmove = self.board[7][0].has_moved
                                    self.cc = 1
                                    self.move_piece(Position(7, 0), Position(7, 3))
                        if self.is_check(self.current_player):
                            if co_1.color == "White":
                                if co_ii == 0:
                                    if j > co_jj:
                                        self.cc = 1
                                        self.move_piece(Position(0, 5), Position(0, 7))
                                        self.board[0][7].has_moved = Hsmove
                                    if j < co_jj:
                                        self.cc = 1
                                        self.move_piece(Position(0, 3), Position(0, 0))
                                        self.board[0][0].has_moved = Hsmove
                            if co_1.color == "Black":
                                if co_ii == 7:
                                    if j > co_jj:
                                        self.cc = 1
                                        self.move_piece(Position(7, 5), Position(7, 7))
                                        self.board[7][7].has_moved = Hsmove
                                    if j < co_jj:
                                        self.cc = 1
                                        self.move_piece(Position(7, 3), Position(7, 0))
                                        self.board[7][0].has_moved = Hsmove


                    temp = False
                    if self.is_check(self.current_player):
                        messagebox.showinfo("NOP", "Your still check")
                        self.remove_piece(self.board[i][j])
                        self.place_piece(co_1, Position(co_ii, co_jj), white)
                        if hmove1 != None:
                            self.board[co_ii][co_jj].has_moved = hmove1
                        self.place_piece(co_2, Position(i, j), white)
                        if hmove2 != None:
                            self.board[i][j].has_moved = hmove2
                        if en_passant:
                            self.place_piece(en_passant_copy, Position(co_ii, j), white)
                        for ii in range(8):
                            for jj in range(8):
                                if self.board[ii][jj]:
                                    if self.board[ii][jj].piece_type == "king" and self.board[ii][jj].color == self.current_player:
                                        self.buttons[ii][jj].config(highlightthickness = 1.2,highlightbackground = '#ff0000')
                        temp = True
                    start_row = 1 if self.current_player == "White" else 6
                    matin = 0
                    if not temp:
                        if self.board[i][j].piece_type == "pawn":
                            if co_ii == start_row:
                                if abs(co_ii - i) > 1:
                                    self.last_piece_move = self.board[i][j]
                                    matin = 1
                        if not matin:
                            self.last_piece_move = None
                        if en_passant:
                            w = Button(master, image = pawnbichare.im1)
                            if pawnbichare.color == "White":
                                if self.remiw < 8:
                                    w.grid(row = self.remiw, column = 8)
                                else:
                                    w.grid(row = self.remiw - 8, column = 9)
                                self.remiw += 1
                            else:
                                if self.remib < 8:
                                    w.grid(row = 8, column = self.remib)
                                else:
                                    w.grid(row = 9, column = self.remib - 8)
                                self.remib += 1
                    
                    if not temp:
                        if self.board[i][j].piece_type == "pawn":
                            if i == 0 or i == 7:
                                global new
                                new = Toplevel(master)
                                new.geometry("220x220")
                                btrook = Button(new, image = Rookblackb, command = chess_game.chess_set.board.inner3(Rook("Black",self,Rookblackw, Rookblackb),i, j,Rookblackb))
                                btknight = Button(new, image = Knightblackb,command = chess_game.chess_set.board.inner3(Knight("Black",self,Knightblackw,Knightblackb),i, j,Knightblackb))
                                btbishop = Button(new, image = Bishopblackb,command = chess_game.chess_set.board.inner3(Bishop("Black",self,Bishopblackw,Bishopblackb), i, j,Bishopblackb))
                                btqueen = Button(new, image = Queenblackb,command = chess_game.chess_set.board.inner3(Queen("Black",self,Queenblackw,Queenblackb),i, j,Queenblackb))
                                btrook1 = Button(new, image = Rookblackw,command = chess_game.chess_set.board.inner3(Rook("Black",self,Rookblackw, Rookblackb),i, j,Rookblackw))
                                btknight1 = Button(new, image = Knightblackw,command = chess_game.chess_set.board.inner3(Knight("Black",self,Knightblackw,Knightblackb),i,j,Knightblackw))
                                btbishop1 = Button(new, image = Bishopblackw,command = chess_game.chess_set.board.inner3(Bishop("Black",self,Bishopblackw,Bishopblackb), i, j,Bishopblackw))
                                btqueen1 = Button(new, image = Queenblackw,command = chess_game.chess_set.board.inner3(Queen("Black",self,Queenblackw,Queenblackb),i, j,Queenblackw))
                                brook = Button(new, image = Rookwhiteb, command = chess_game.chess_set.board.inner3(Rook("White",self,Rookwhitew, Rookwhiteb),i, j,Rookwhiteb))
                                bknight = Button(new, image = Knightwhiteb, command = chess_game.chess_set.board.inner3(Knight("White",self,Knightwhitew,Knightwhiteb),i,j,Knightwhiteb))
                                bbishop = Button(new, image = Bishopwhiteb,command = chess_game.chess_set.board.inner3(Bishop("White",self,Bishopwhitew,Bishopwhiteb), i, j,Bishopwhiteb))
                                bqueen = Button(new, image = Queenwhiteb,command = chess_game.chess_set.board.inner3(Queen("White",self,Queenwhitew,Queenwhiteb),i, j,Queenwhiteb))
                                brook1 = Button(new, image = Rookwhitew,command = chess_game.chess_set.board.inner3(Rook("White",self,Rookwhitew, Rookwhiteb),i, j,Rookwhitew))
                                bknight1 = Button(new, image = Knightwhitew,command = chess_game.chess_set.board.inner3(Knight("White",self,Knightwhitew,Knightwhiteb),i,j,Knightwhitew))
                                bbishop1 = Button(new, image = Bishopwhitew,command = chess_game.chess_set.board.inner3(Bishop("White",self,Bishopwhitew,Bishopwhiteb), i, j,Bishopwhitew))
                                bqueen1 = Button(new, image = Queenwhitew,command = chess_game.chess_set.board.inner3(Queen("White",self,Queenwhitew,Queenwhiteb),i, j,Queenwhitew))
                            if self.board[i][j].color == "Black":
                                if i == 0:
                                    if (i + j) % 2:
                                        btrook.grid(row = 0, column = 0)
                                        btknight.grid(row = 0, column = 1)
                                        btbishop.grid(row = 1, column = 0)
                                        btqueen.grid(row = 1, column = 1)
                                    else:
                                        btrook1.grid(row = 0, column = 0)
                                        btknight1.grid(row = 0, column = 1)
                                        btbishop1.grid(row = 1, column = 0)
                                        btqueen1.grid(row = 1, column = 1)
                                    
                            else:
                                if i == 7:
                                    if (i + j) % 2:
                                        brook.grid(row = 0, column = 0)
                                        bknight.grid(row = 0, column = 1)
                                        bbishop.grid(row = 1, column = 0)
                                        bqueen.grid(row = 1, column = 1)
                                    else:
                                        brook1.grid(row = 0, column = 0)
                                        bknight1.grid(row = 0, column = 1)
                                        bbishop1.grid(row = 1, column = 0)
                                        bqueen1.grid(row = 1, column = 1)
                    self.current_player = "Black" if self.current_player == "White" else "White"
                    enemy = "Black" if self.current_player == "White" else "White"
                    if temp == True:
                        self.current_player = "Black" if self.current_player == "White" else "White"
                    eee = 0
                    end = 0
                    if self.is_checkmate(self.current_player):
                        messagebox.showinfo("The end", f'{self.current_player} wins')
                        for ii in range(8):
                            for jj in range(8):
                                if self.board[ii][jj]:
                                    if self.board[ii][jj].piece_type == "king" and self.board[ii][jj].color == self.current_player:
                                        self.buttons[ii][jj].config(highlightthickness = 1.2,highlightbackground = '#ff0000')
                        end = 1
                        master.destroy()
                    if self.is_check(self.current_player) and not temp and not end:
                        messagebox.showinfo("check", f'{enemy} is check')
                        for ii in range(8):
                            for jj in range(8):
                                if self.board[ii][jj]:
                                    if self.board[ii][jj].piece_type == "king" and self.board[ii][jj].color == self.current_player:
                                        self.buttons[ii][jj].config(highlightthickness = 1.2,highlightbackground = '#ff0000')
        return rgt
    def inner3(self, piece, i, j, img):
        def click():
            self.buttons[i][j].config(image = img)
            self.board[i][j] = piece
            self.board[i][j].position = Position(i, j)
            new.destroy()

            

        return click     
    def is_check(self, current_player):
        enemy = "Black" if current_player == "White" else "White"
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece:
                    if piece.color == enemy:
                        if piece.possible_moves():
                            for pos in piece.possible_moves():
                                if self.board[pos.row][pos.col]:
                                    if self.board[pos.row][pos.col].piece_type == "king":
                                        return True
            
        return False
    def is_checkmate(self, current_player):
        enemy = "Black" if current_player == "White" else "White"
        if not self.is_check(current_player):
            return False
        for i in range(8):
            for j in range(8):
                if not self.board[i][j]:
                    continue
                if self.board[i][j].color == enemy:
                    continue
                co_1 = self.board[i][j]
                for mv in self.board[i][j].possible_moves():
                    self.ischecking = True
                    co_2 = self.board[mv.row][mv.col]
                    if co_1:
                        help1 = self.board[i][j].has_moved
                    if co_2:
                        help2 = self.board[i][j].has_moved
                    if co_1.piece_type == "king" and abs(j - mv.col) > 1:
                        continue
                    self.move_piece(Position(i, j), mv)
                    hsmove = None
                    if j - mv.col == 2 and co_1.piece_type == "king":
                        self.cc = 1
                        if co_1.color == "White":
                            hsmove = self.board[0][0].has_moved
                            self.move_piece(Position(0, 0), Position(0, 3))
                        else:
                            hsmove = self.board[7][0].has_moved
                            self.move_piece(Position(7, 0), Position(7, 3))
                    if j - mv.col == -2 and co_1.piece_type == "king":
                        self.cc = 1
                        if co_1.color == "White":
                            hsmove = self.board[0][7].has_moved
                            self.move_piece(Position(0, 7), Position(0, 5))
                        else:
                            hsmove = self.board[7][7].has_moved
                            self.move_piece(Position(7,7), Position(7,5))
                    if not self.is_check(current_player):
                        self.remove_piece(self.board[mv.row][mv.col])
                        self.place_piece(co_1, Position(i, j), co_1.im1)
                        if co_2:
                            self.place_piece(co_2, Position(mv.row, mv.col), co_2.im1)
                        else:
                            self.place_piece(co_2, Position(mv.row, mv.col), white)
                        if self.board[i][j]:
                            self.board[i][j].has_moved = help1
                        if self.board[mv.row][mv.col]:
                            self.board[mv.row][mv.col].has_moved = help2
                        if j - mv.col == 2 and co_1.piece_type == "king":
                            if co_1.color == "White":
                                self.move_piece(Position(0, 3), Position(0, 0))
                                self.board[0][0].has_moved = hsmove
                            else:
                                self.move_piece(Position(7, 3), Position(7, 0))
                                self.board[7][0].has_moved = hsmove
                        if j - mv.col == -2 and co_1.piece_type == "king":
                            if co_1.color == "White":
                                self.move_piece(Position(0, 5), Position(0, 7))
                                self.board[0][7].has_moved = hsmove
                            else:
                                self.move_piece(Position(7,5), Position(7,7))
                                self.board[7][7].has_moved = hsmove
                        self.ischecking = False
                        return False
                    if j - mv.col == 2 and co_1.piece_type == "king":
                        if co_1.color == "White":
                            self.move_piece(Position(0, 3), Position(0, 0))
                            self.board[0][0].has_moved = hsmove
                        else:
                            self.move_piece(Position(7, 3), Position(7, 0))
                            self.board[7][0].has_moved = hsmove
                    if j - mv.col == -2 and co_1.piece_type == "king":
                        if co_1.color == "White":
                            self.move_piece(Position(0, 5), Position(0, 7))
                            self.board[0][7].has_moved = hsmove
                        else:
                            self.move_piece(Position(7,5), Position(7,7))
                            self.board[7][7].has_moved = hsmove
                    self.remove_piece(self.board[mv.row][mv.col])
                    self.place_piece(co_1, Position(i, j), co_1.im1)
                    if co_2:
                        self.place_piece(co_2, Position(mv.row, mv.col), co_2.im1)
                    else:
                        self.place_piece(co_2, Position(mv.row, mv.col), white)
                    if self.board[i][j]:
                        self.board[i][j].has_moved = help1
                    if self.board[mv.row][mv.col]:
                        self.board[mv.row][mv.col].has_moved = help2
                self.ischecking = False
        return True
    def place_piece(self, piece, position, pic):
        if piece:
            self.board[position.row][position.col] = piece
        if piece:
            tmp = 'green' if piece.color == "White" else 'black'
        else:
            tmp = 'white'
        if piece:
            if (position.row + position.col) % 2:
                self.buttons[position.row][position.col].config(foreground = tmp, image = piece.im2)
            else:
                self.buttons[position.row][position.col].config(foreground = tmp, image = piece.im1)
            piece.position = position
        else:
            if ((position.row + position.col) % 2 == 0):
                self.buttons[position.row][position.col].config(image = white)
            else:
                self.buttons[position.row][position.col].config(image = blue)
                

    def remove_piece(self, piece):
        self.board[piece.position.row][piece.position.col] = None
        if ((piece.position.row + piece.position.col) % 2 == 0):
            self.buttons[piece.position.row][piece.position.col].config(image = white)
        else:
            self.buttons[piece.position.row][piece.position.col].config(image = blue)

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos.row][start_pos.col]
        if not self.ischecking and self.board[end_pos.row][end_pos.col]:
            w = Button(master, image = self.board[end_pos.row][end_pos.col].im1)
            if self.board[end_pos.row][end_pos.col].color == 'White':
                if self.remiw < 8:
                    w.grid(row = self.remiw, column = 8)
                else:
                    w.grid(row = self.remiw - 8, column = 9)
                self.remiw += 1
            else:
                if self.remib < 8:
                    w.grid(row = 8, column = self.remib)
                else:
                    w.grid(row = 9, column = self.remib - 8)
                self.remib += 1
        if piece:
            if piece.move(end_pos) or (piece.piece_type == 'rook' and self.cc == 1):
                if piece.piece_type == 'rook' and self.cc == 1:
                    self.cc = 0
                self.remove_piece(piece)
                piece.has_moved = True
                piece.position = end_pos
                self.place_piece(piece, end_pos, piece.im1)
                return True
        else:
            return False

    def is_square_empty(self, position):
        return self.board[position.row][position.col] is None

    def is_enemy_piece(self, position, color):
        if not self.is_square_empty(position):
            if self.board[position.row][position.col].color == color:
                return False
            return True
        return False
            


    def is_inside_board(self, position):
        if position.row > 7 or position.col > 7 or position.row < 0 or position.col < 0:
            return False
        return True
class ChessSet:
    def __init__(self):
        self.board = Board()
        self.setup_board()

    def setup_board(self):
        # Place white pieces
        self.board.place_piece(Rook("White",self.board,Rookwhitew, Rookwhiteb), Position(0, 0), Rookwhitew)
        self.board.place_piece(Knight("White",self.board, Knightwhitew,Knightwhiteb), Position(0, 1), Knightwhiteb)
        self.board.place_piece(Bishop("White",self.board,Bishopwhitew,Bishopwhiteb), Position(0, 2), Bishopwhitew)
        self.board.place_piece(Queen("White",self.board,Queenwhitew,Queenwhiteb), Position(0, 3), Queenwhitew)
        self.board.place_piece(King("White",self.board,Kingwhitew, Kingwhiteb), Position(0, 4),Kingwhiteb)
        self.board.place_piece(Bishop("White",self.board, Bishopwhitew,Bishopwhiteb), Position(0, 5), Bishopwhiteb)
        self.board.place_piece(Knight("White",self.board,Knightwhitew,Knightwhiteb), Position(0, 6), Knightwhitew)
        self.board.place_piece(Rook("White",self.board,Rookwhitew,Rookwhiteb), Position(0, 7), Rookwhiteb)
        for col in range(8):
            if col % 2 == 0:
                self.board.place_piece(Pawn("White", self.board,Pawnwhitew,Pawnwhiteb), Position(1, col), Pawnwhiteb)
            else:
                self.board.place_piece(Pawn("White", self.board,Pawnwhitew,Pawnwhiteb), Position(1, col), Pawnwhitew)


        # Place black pieces
        self.board.place_piece(Rook("Black",self.board,Rookblackw, Rookblackb), Position(7, 0), Rookblackb)
        self.board.place_piece(Knight("Black",self.board,Knightblackw,Knightblackb), Position(7, 1), Knightblackw)
        self.board.place_piece(Bishop("Black",self.board,Bishopblackw,Bishopblackb), Position(7, 2), Bishopblackb)
        self.board.place_piece(Queen("Black",self.board,Queenblackw,Queenblackb), Position(7, 3), Queenblackw)
        self.board.place_piece(King("Black",self.board,Kingblackw,Kingblackb), Position(7, 4),Kingblackw)
        self.board.place_piece(Bishop("Black",self.board,Bishopblackw,Bishopblackb), Position(7, 5), Bishopblackw)
        self.board.place_piece(Knight("Black",self.board,Knightblackw,Knightblackb), Position(7, 6), Knightblackb)
        self.board.place_piece(Rook("Black",self.board,Rookblackw,Rookblackb), Position(7, 7), Rookblackw)
        for col in range(8):
            if col % 2 == 0:
                self.board.place_piece(Pawn("Black", self.board,Pawnblackw,Pawnblackb), Position(6, col), Pawnblackw)
            else:
                self.board.place_piece(Pawn("Black", self.board,Pawnblackw,Pawnblackb), Position(6, col), Pawnblackb)
class Chess:
    def __init__(self):
        self.chess_set = ChessSet()

if __name__ == "__main__":
    master = tk.Tk()
    master.geometry("1000x850")
    master.resizable(False, False)
    master["bg"] = "#000000"
    Rookwhitew = ImageTk.PhotoImage(Image.open(r"chess_pieces/1_Rookwhitew.jpg").resize((80,80)))
    Rookwhiteb = ImageTk.PhotoImage(Image.open(r"chess_pieces/2_rookwhiteb.jpg").resize((80,80)))
    Rookblackw = ImageTk.PhotoImage(Image.open(r"chess_pieces/3_rookblackw.jpg").resize((80,80)))
    Rookblackb = ImageTk.PhotoImage(Image.open(r"chess_pieces/4_rookblackb.jpg").resize((80,80)))
    Bishopwhitew = ImageTk.PhotoImage(Image.open(r"chess_pieces/5_Bishopwhitew.jpg").resize((80,80)))
    Bishopwhiteb = ImageTk.PhotoImage(Image.open(r"chess_pieces/6_Bishopwhiteb.jpg").resize((80,80)))
    Bishopblackw = ImageTk.PhotoImage(Image.open(r"chess_pieces/7_Bishopblackw.jpg").resize((80,80)))
    Bishopblackb = ImageTk.PhotoImage(Image.open(r"chess_pieces/8_Bishopblackb.jpg").resize((80,80)))
    Knightwhitew = ImageTk.PhotoImage(Image.open(r"chess_pieces/9_Knightwhitew.jpg").resize((80,80)))
    Knightwhiteb = ImageTk.PhotoImage(Image.open(r"chess_pieces/10_Knightwhiteb.jpg").resize((80,80)))
    Knightblackw = ImageTk.PhotoImage(Image.open(r"chess_pieces/11_Knightblackw.jpg").resize((80,80)))
    Knightblackb = ImageTk.PhotoImage(Image.open(r"chess_pieces/12_Knightblackb.jpg").resize((80,80)))
    Pawnwhitew = ImageTk.PhotoImage(Image.open(r"chess_pieces/13_Pawnwhitew.jpg").resize((80,80)))
    Pawnwhiteb = ImageTk.PhotoImage(Image.open(r"chess_pieces/14_Pawnwhiteb.jpg").resize((80,80)))
    Pawnblackw = ImageTk.PhotoImage(Image.open(r"chess_pieces/15_Pawnblackw.jpg").resize((80,80)))
    Pawnblackb = ImageTk.PhotoImage(Image.open(r"chess_pieces/16_Pawnblackb.jpg").resize((80,80)))
    Queenwhitew = ImageTk.PhotoImage(Image.open(r"chess_pieces/17_Queenwhitew.jpg").resize((80,80)))
    Queenwhiteb = ImageTk.PhotoImage(Image.open(r"chess_pieces/18_Queenwhiteb.jpg").resize((80,80)))
    Queenblackb = ImageTk.PhotoImage(Image.open(r"chess_pieces/20_Queenblackb.jpg").resize((80,80)))
    Queenblackw = ImageTk.PhotoImage(Image.open(r"chess_pieces/21_Queenblackw.jpg").resize((80,80)))
    Kingwhiteb = ImageTk.PhotoImage(Image.open(r"chess_pieces/23_Kingwhiteb.jpg").resize((80,80)))
    Kingwhitew = ImageTk.PhotoImage(Image.open(r"chess_pieces/22_Kingwhitew.jpg").resize((80,80)))
    Kingblackw = ImageTk.PhotoImage(Image.open(r"chess_pieces/24_Kingblackw.jpg").resize((80,80)))
    Kingblackb = ImageTk.PhotoImage(Image.open(r"chess_pieces/25_Kingblackb.jpg").resize((80,80)))
    white = ImageTk.PhotoImage(Image.open(r"chess_pieces/white.jpg").resize((80,80)))
    blue = ImageTk.PhotoImage(Image.open(r"chess_pieces/blue.jpg").resize((80,80)))
    chess_game = Chess()
    master.mainloop()
