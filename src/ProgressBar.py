import os

def show_progress_bar(state, end, accuracy=20, **kwargs):
   os.system('cls')
   try:
      print(kwargs['data'], end='\n\n')
   except:
      print(end='\n\n')
   try: 
      print(f"{kwargs['name']}:")
   except:
      print("Unknown:")
   percentage = (state * 100) / end
   print('[', end='')
   for n in range(accuracy):
      if state < n * (end / accuracy):
         print('.', end='')
      else:
         print('#', end='')
   print(']', '    ', f"{percentage:.1f}", '%')

def progress_bar_buffer(state, end, accuracy=20, **kwargs):
   os.system('cls')
   buffer = f""
   try:
      buffer += f"{kwargs['data']}\n\n"
   except:
      buffer += f"\n\n"
   try: 
      buffer += f"{kwargs['name']}:\n"
   except:
      buffer += f"Unknown:\n"
   percentage = (state * 100) / end
   buffer += f"["
   for n in range(accuracy):
      if state < n * (end / accuracy):
         buffer += f"."
      else:
         buffer += f"#"
   buffer += f"]\t{percentage:.1f} %"
   return buffer