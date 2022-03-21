import msvcrt, time, threading, multiprocessing   # modules to handle input properly
import os, random, json, sys                      # modules for random stuff
import MenuMaker, ProgressBar                     # custom modules

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

   # rotating right the piece means reversing the columns and turning them into a row in the new rotated piece,
   # same thing for turning left, but without reversing every column
   @staticmethod
   def rotate_piece(piece, arr, _dir):
      if piece is not None and arr is None:
         if _dir == 'right':
            new_piece = []
            for n in range(len(piece.piece[0])): # 0 -> len(arr)
               # the column is reversed
               new_row = Tetromino.get_col(n, piece.piece)[::-1]
               new_piece.append(new_row)
         if _dir == 'left':
            new_piece = []
            for n in range(-1, (-len(piece.piece[0]))-1, -1): # -1 -> -len(arr)
               # the column is not reversed
               new_row = Tetromino.get_col(n, piece.piece)[::1]
               new_piece.append(new_row)
         return new_piece
      elif piece is None and arr is not None:
         if _dir == 'right':
            new_arr = []
            for n in range(len(arr[0])):
               # the column is reversed
               new_row = Tetromino.get_col(n, arr)[::-1]
               new_arr.append(new_row)
         if _dir == 'left':
            new_arr = []
            for n in range(-1, (-len(arr[0]))-1, -1): # len(arr) -> 0
               # the column is not reversed
               new_row = Tetromino.get_col(n, arr)[::1]
               new_arr.append(new_row)
         return new_arr
   
   # idk maybe they're useful
   @staticmethod
   def get_row(n, arr):
      return arr[n]
   @staticmethod
   def get_col(n, arr):
      return [row[n] for row in arr]



class Tetris:
   # O======================================O
   # |            SETUP METHODS             |
   # O======================================O

   # initialize the board data list ('#' -> occupied ; '.' -> empty),
   # holds the current piece 
   # and the data which the pieces are formed with
   def __init__(self, speed_lvl:int=0):
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
      self.game_over = False
      self.score = 0
      self.score_per_line = 32
      self.score_per_place = 15
      self.speed = [1.0, 0.9, 0.8, 0.7, 0.5, 0.3][speed_lvl]
      self.user_input = None
   
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
         #new_piece = Tetromino(self.pieces_data['square'], len(self.board[0]), coords)
         new_piece = Tetromino(self.pieces_data[random.choice(list(self.pieces_data.keys()))], len(self.board[0]), coords)
         if not self.check_collisions(new_piece, 'place', None):
            return new_piece
         else:
            self.game_over = True
      else:
         new_piece = Tetromino(shape, len(self.board[0]), coords)
         if not self.check_collisions(new_piece, 'place', None):
            return new_piece
         else:
            self.game_over = True


   # if the piece collides with other blocks, than it cant be moved
   def check_collisions(self, piece, movement:str, rotation:str) -> bool:
      if (movement is not None) and (rotation is None):
         if movement == 'down':
            for row in range(len(piece.piece)):
               for col in range(len(piece.piece[row])):
                  # if the piece goes too down, it's a collision
                  if row + piece.pos.y >= len(self.board)-1:
                     return True
                  # if the piece encounter another block on the board, it's a collision
                  if self.board[piece.pos.y + row + 1][piece.pos.x + col] == '#' and piece.piece[row][col] == '#':
                     return True
         if movement == 'left':
            for row in range(len(piece.piece)):
               for col in range(len(piece.piece[row])):
                  # if the piece goes too far to the left, it's a collision
                  if col + piece.pos.x - 1 < 0:
                     return True
                  # if the piece encounter another block on the board, it's a collision
                  if self.board[piece.pos.y + row][piece.pos.x + col - 1] == '#' and piece.piece[row][col] == '#':
                     return True
         if movement == 'right':
            for row in range(len(piece.piece)):
               for col in range(len(piece.piece[row])):
                  # if the piece goes too far to the right, it's a collision
                  if col + piece.pos.x + 1 > len(self.board[0]) - 1:
                     return True
                  # if the piece encounter another block on the board, it's a collision
                  if self.board[piece.pos.y + row][piece.pos.x + col + 1] == '#' and piece.piece[row][col] == '#':
                     return True
         if movement == 'place':
            for row in range(len(piece.piece)):
               for col in range(len(piece.piece[row])):
                  # if the piece encounter another block on the board, it's a collision
                  if self.board[piece.pos.y + row][piece.pos.x + col + 1] == '#' and piece.piece[row][col] == '#':
                     return True
      elif (movement is None) and (rotation is not None):
         temp_piece = Tetromino.rotate_piece(None, self.current_piece.piece, rotation)
         for row in range(len(temp_piece)):
               for col in range(len(temp_piece[row])):
                  # if the piece goes too far to the right, it's a collision
                  if col + self.current_piece.pos.x + 1 > len(self.board[0]) - 1:
                     return True
                  # if the piece goes too far to the left, it's a collision
                  if col + self.current_piece.pos.x - 1 < 0:
                     return True
                  # if the piece encounter another block on the board, it's a collision
                  if self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col + 1] == '#' and self.current_piece.piece[row][col] == '#':
                     return True
      return False

   # given that the piece is safe to place, sets the corresponding blocks to '#' (occupied, empty is '.')
   def place_piece(self, piece: Tetromino) -> None:
      # place a block at the corresponding coordinates for every piece block
      for i in range(len(piece.piece)):
         for j in range(len(piece.piece[i])):
            if piece.piece[i][j] == '#': self.board[piece.pos.y+i][piece.pos.x+j] = '#'
            self.score += (self.score_per_place - piece.pos.y + len(piece.piece))
      # then creates a new piece that will appear on the top
      self.current_piece = self.create_piece()
   
   # if the position is safe, moves the piece's position down by 1,
   # otherwise, place the piece
   def move_piece(self, direction) -> None:
      # check the collision in the given directoin
      collision = self.check_collisions(self.current_piece, direction, None)
      # perform the movement for the right direction if the collision didn't occur
      if direction == 'down':
         if collision == False: self.current_piece.pos.y += 1
         elif collision == True: # in this case it place the block rather than stopping the movement
            self.place_piece(self.current_piece)
      if direction == 'left':
         if collision == False: self.current_piece.pos.x -= 1
      if direction == 'right':
         if collision == False: self.current_piece.pos.x += 1
      
   def rotate_piece(self, direction: str) -> None:
      # there's a bug i have to resolve
      try:
         collision = self.check_collisions(self.current_piece, None, direction)
         if not collision:
            self.current_piece.piece = Tetromino.rotate_piece(self.current_piece, None, direction)
      except:
         self.current_piece.piece = Tetromino.rotate_piece(self.current_piece, None, direction)
   
   def check_lines(self):
      lines = []
      for row in range(len(self.board)):
         if all(x == '#' for x in self.board[row]):
            lines.append(self.board[row])
            for block in range(len(self.board[row])): self.board[row][block] = '.'
      if len(lines) != 0:
         self.move_lines(lines)
      line_counter = 1
      for line in lines:
         self.score += self.score_per_line * line_counter
         line_counter += 5 # the score rise quickly if there is more than one line

   def move_lines(self, lines) -> None:
      # there are some bugs to fix
      try:
         for row in range(-2, (-len(self.board))-1, -1):
            if any(x == '#' for x in self.board[row]):
               for block in range(len(self.board[row])):
                  self.board[row+len(lines)][block] = self.board[row][block]
                  self.board[row][block] = self.board[row-len(lines)][block]
      except: pass


   # show the board data AND the current piece data on top
   def show_board(self) -> None:
      os.system("cls")
      print(f"Score:   {self.score}", end='\n\n')
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
                  if self.current_piece.piece[row][col] == '#' and self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col] != '#':
                     self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col] = "@"
         # at the end of the printing session, it removese the placeholders to clear the board
         elif action == 'remove':
            for row in range(len(self.current_piece.piece)):
               for col in range(len(self.current_piece.piece[row])):
                  if self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col] == "@":
                     self.board[self.current_piece.pos.y + row][self.current_piece.pos.x + col] = "."
      except: pass
   
   def main_loop(self) -> None:
      while not self.game_over:
         self.event_queue.append('v') # automatic vertical movement
         self.show_board()
         self.execute_event_queue() # 1
         time.sleep(self.speed)
         self.execute_event_queue() # 2
         self.check_lines()
         self.execute_event_queue() # 3
      else:
         self.game_over_screen()
   
   # this will run in a separate thread, therefor will be constantly checking for input
   def take_input(self) -> None:
      while not self.game_over:
         action = msvcrt.getch()
         # commands for movement, harddrop, and quit
         if action == b'j': self.event_queue.append('l')    # left
         if action == b'l': self.event_queue.append('r')    # right
         if action == b'a': self.event_queue.append('rl')   # rotate left
         if action == b'd': self.event_queue.append('rr')   # rotate right
         if action == b'q': self.event_queue.append('q')    # pause
         if action == b'k': 
            for _ in range(5): self.event_queue.append('v')   # hard drop
      else:
         self.game_over_screen()
   
   def execute_event_queue(self) -> None:
      for event in self.event_queue:
         if event == 'v':
            self.move_piece('down')
         if event == 'r':
            self.move_piece('right')
         if event == 'l':
            self.move_piece('left')
         if event == 'rl':
            self.rotate_piece('left')
         if event == 'rr':
            self.rotate_piece('right')
         if event == 'q':
            a = input()
      self.event_queue.clear()
   
   def game_over_screen(self):
      os.system('cls')
      print("You're a damn loser!", end='\n\n')
      print(f"Your Score: {self.score}")



#Tetris(3).run()


# O=============================O
# |      Bad Menu System        |
# O=============================O

def start():
   for i in range(60):
      ProgressBar.show_progress_bar(i, 60, 40, name="Loading")
   Tetris(3).run()

def rules():
   os.system('cls')
   print("It's fucking tetris, dickhead!")
   print("Move with J (left) - K (hard drop) - L (right)")
   print("Rotate with A (counter c.w.) - D (c.w.)")

def quit_():
   sys.exit()

menu1_f = start
menu1_lbl = "Play"
menu2_f = rules
menu2_lbl = "Rules"
menu3_f = quit_
menu3_lbl = "Quit"

menu = MenuMaker.Menu([menu1_lbl, menu2_lbl, menu3_lbl], [menu1_f, menu2_f, menu3_f])