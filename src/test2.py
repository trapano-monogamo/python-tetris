arr = [
   [1,2,3],
   [4,5,6]
]

new_arr = [['.' for _ in range(len(arr))] for _ in range(len(arr[0]))]

print(arr, '\n\n', new_arr)