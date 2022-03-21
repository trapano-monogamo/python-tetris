def rotate1(arr) -> None: # RIGHT
   new_arr = [['.' for _ in range(len(arr))] for _ in range(len(arr[0]))]
   for n in range(len(arr[0])):
      # the column is reversed
      new_row = __get_col(n, arr)[::-1]
      new_arr[n] = new_row
   return new_arr

def rotate2(arr): # LEFT
   new_arr = [['.' for _ in range(len(arr))] for _ in range(len(arr[0]))]
   for n in range(-1, (-len(arr[0]))-1, -1): # len(arr) -> 0
      # the column is not reversed
      new_row = __get_col(n, arr)[::1]
      new_arr[(-n)-1] = new_row
   return new_arr

def __get_col(n, arr):
   return [row[n] for row in arr]

def change(arr):
   return arr.clear()

arr = [
   [1],
   [2],
   [3],
   [4]
]
arr2 = change(arr) # cazzoooooooo
print(arr, arr2)
#print(arr, '\n', rotate1(arr), '\n', rotate2(arr))