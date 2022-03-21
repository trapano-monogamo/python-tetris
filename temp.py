import msvcrt, time, threading, multiprocessing   # modules to handle input properly
import os, random, json, sys                      # modules for random stuff

# why? because!
# this way i can get the pos of a piece by its {x,y} coords
class Coord:
   def __init__(self, _x, _y):
      self.x = _x
      self.y = _y

# a class that holds the piece structure, its position,
# and the method to turn it right or left.
class Tetromino:
   def __init__(self, shape:list, pos_limit_x:int=None, coords:Coord=None):
      self.piece = shape
      if coords is None:
         self.pos = Coord((pos_limit_x//2)-1, 0)
      else:
         self.fake_pos = coords

   # liner algebra maths goes brrrrrrr
   def rotate_piece(self, dir) -> None:
      pass



class Tetris:
   # O======================================O
   # |            SETUP METHODS             |
   # O======================================O

   # initialize the board data list ('#' -> occupied ; '.' -> empty),
   # holds the current piece 
   # and the data which the pieces are formed with
   def __init__(self, _compact=False):
      """
      Tetris class structure
         / pre-game
            - get the pieces' shapes
         / during game methods
            - draw the board
            / move current piece
               - check if position is safe
               - move down the piece every "turn"
               - if needed, rotate the piece ("move current piece" with needed checks)
         / logic
            - get user input
            - manage timing
            - "during game methods" management
      """
      self.rows = 18 ; self.cols = 12
      self.board = [['.' for col in range(self.cols)] for row in range(self.rows)]
      self.pieces_data = self.get_pieces()
      self.current_piece = self.create_piece()
      self.event_queue = []
      self.user_input = None
      self.compact = _compact
   
   # parse the json file to get the possible piece shapes
   def get_pieces(self) -> dict:
      with open('./src/shapes.json', 'r') as f:
         data = json.load(f)
      f.close()
      return data

   # create a parallel thread to handle input without
   # interrupting the game, then it starts the game
   def run(self) -> None:
      self.user_input = threading.Thread(target=self.take_input)
      self.user_input.start()
      self.main_loop()
      


   # O======================================O
   # |        GAME LOGIC METHODS            |
   # O======================================O

   # create a Tetromino with a random shape
   # don't ask anything... idk
   def create_piece(self, shape=None, coords=None) -> Tetromino:
      if shape == None:
         return Tetromino(self.pieces_data[random.choice(list(self.pieces_data.keys()))], len(self.board[0]), coords)
      else:
         return Tetromino(shape, len(self.board[0]), coords)


   # if the piece collides with other blocks, than it cant be moved
   def check_collisions(self, movement: str) -> bool:
      if movement == 'down':
         for row in range(len(self.current_piece.piece)):
            for col in range(len(self.current_piece.piece[row])):
               # if the piece goes too down, it's a collision
               if row + self.current_piece.pos.y >= len(self.board)-1:
                  return True
               # if the piece encounter another block on the board, it's a collision
               if self.board[self.current_piece.pos.y + row + 1][self.current_piece.pos.x + col] == '#':
                  return True
      if movement == 'left':
         for row in range(len(self.current_piece.piece)):
            for col in range(len(self.current_piece.piece[row])):
               # if the piece goes too far to the left, it's a collision
               if col + self.current_piece.pos.x - 1 < 0:
                  return True
               # if the piece encounter another block on the board, it's a collision
               if self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col - 1] == '#':
                  return True
      if movement == 'right':
         for row in range(len(self.current_piece.piece)):
            for col in range(len(self.current_piece.piece[row])):
               # if the piece goes too far to the right, it's a collision
               if col + self.current_piece.pos.x + 1 > len(self.board[0]) - 1:
                  return True
               # if the piece encounter another block on the board, it's a collision
               if self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col + 1] == '#':
                  return True
      return False

   # given that the piece is safe to place, sets the corresponding blocks to '#' (occupied, empty is '.')
   def place_piece(self, piece: Tetromino) -> None:
      # place a block at the corresponding coordinates for every piece block
      for i in range(len(piece.piece)):
         for j in range(len(piece.piece[i])):
            if piece.piece[i][j] == '#': self.board[piece.pos.y+i][piece.pos.x+j] = '#'
      # then creates a new piece that will appear on the top
      self.current_piece = self.create_piece()
   
   # if the position is safe, moves the piece's position down by 1,
   # otherwise, place the piece
   def move_piece(self, direction) -> None:
      # check the collision in the given directoin
      collision = self.check_collisions(direction)
      # perform the movement for the right direction if the collision didn't occur
      if direction == 'down':
         if collision == False: self.current_piece.pos.y += 1
         elif collision == True: # in this case it place the block rather than stopping the movement
            self.place_piece(self.current_piece)
      if direction == 'left':
         if collision == False: self.current_piece.pos.x -= 1
      if direction == 'right':
         if collision == False: self.current_piece.pos.x += 1

   # show the board data AND the current piece data on top
   def show_board(self) -> None:
      os.system("cls")
      if self.compact:
         self.piece_repr('place')
         for i in range(len(self.board)):
            print('|', end='')
            for j in range(len(self.board[i])):
               if self.board[i][j] == '#' or self.board[i][j] == '@':
                  print('#', end='')
               else:
                  print('.', end='')
            print('|', end='\n')
         print('O', end='')
         for _ in range(len(self.board[0])): print('=', end='')
         print('O', end='\n')
         self.piece_repr('remove')
      elif not self.compact:
         self.piece_repr('place')
         for i in range(len(self.board)):
            print('|', end=' ')
            for j in range(len(self.board[i])):
               if self.board[i][j] == '#' or self.board[i][j] == '@':
                  print('#', end=' ')
               else:
                  print('.', end=' ')
            print('|', end='\n')
         print('O', end='=')
         for _ in range(len(self.board[0])): print('==', end='')
         print('O', end='\n')
         self.piece_repr('remove')

   def piece_repr(self, action: str) -> None:
      try:
         # for every piece block, place a placeholder in the board
         if action == 'place':
            for row in range(len(self.current_piece.piece)):
               for col in range(len(self.current_piece.piece[row])):
                  if self.current_piece.piece[row][col] == '#': # avoid empty spaces in the blocks
                     self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col] = "@"
         # at the end of the printing session, it removese the placeholders to clear the board
         elif action == 'remove':
            for row in range(len(self.current_piece.piece)):
               for col in range(len(self.current_piece.piece[row])):
                  self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col] = "."
      except: pass
   
   def main_loop(self) -> None:
      while not self.game_over():
         self.event_queue.append('v') # automatic vertical movement
         self.show_board()
         time.sleep(0.6)
         self.execute_event_queue()

   # guess what? you're right, this method checks whether you lose or not
   def game_over(self) -> bool:
      return False
   
   # this will run in a separate thread, therefor will be constantly checking for input
   def take_input(self) -> None:
      while not self.game_over():
         action = msvcrt.getch()
         # commands for movement, harddrop, and quit
         if action == b'j': self.event_queue.append('l')    # left
         if action == b'l': self.event_queue.append('r')    # right
         if action == b'k': self.event_queue.append('hd')   # hard drop
         if action == b'q': self.event_queue.append('q')    # quit
   
   def execute_event_queue(self) -> None:
      for event in self.event_queue:
         if event == 'v':
            self.move_piece('down')
         if event == 'r':
            self.move_piece('right')
         if event == 'l':
            self.move_piece('left')
         if event == 'hd':
            pass
         if event == 'q':
            sys.exit()
      self.event_queue.clear()

game = Tetris()
game.run()