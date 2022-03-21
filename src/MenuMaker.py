import msvcrt, os, sys

class Menu:
    def __init__(self, lbls, funcs):
        self.lbls = lbls
        self.funcs = funcs
        self.pos = 0
        self.display()
        self.update_choice()
    
    def update_choice(self):
        choice = msvcrt.getch()
        if choice == b's': # update the choice indicator
            self.pos += 1
        elif choice == b'w':
            self.pos -= 1
        elif choice == b'd': # call the function of the label
            self.apply()
        else: pass
        if self.pos >= len(self.lbls): # choice boundaries
            self.pos = 0
        elif self.pos < 0:
            self.pos = len(self.lbls) - 1
        self.display() # update menu
    
    def display(self):
        os.system('cls')
        current_cell= "-"
        for lbl in self.lbls: # print every label with the cursor (if it is in position)
            if self.pos == self.index_of(lbl, self.lbls):
                current_cell = "> "
            print(f"{current_cell} {lbl}")
            current_cell = "-" # reset cursor for the next label
        self.update_choice()
    
    def index_of(self, elem, arr):
        for x in range(len(arr)): # search element index
            if arr[x] == elem:
                return x
        return -1 # not found
    
    def apply(self):
        self.funcs[self.pos]()
        self.update_choice()

#
#def _exit():
#    os.system('clear')
#    sys.exit()
#
#def _help():
#    os.system('clear')
#    print("This is a demo of my custom menu system.")
#
#def _credits():
#    os.system('clear')
#    print("CREDITS\n")
#    print("Created by: Me\nCoded by: Me\nStyle: Me\nSound: Fuck I knew I was mssing something...")
#
#def _next():
#    global menu_num
#    menu_num += 1
#    menu = Menu(menus[menu_num]['labels'], menus[menu_num]['functions'])
#
#def _back():
#    global menu_num
#    menu_num -= 1
#    menu = Menu(menus[menu_num]['labels'], menus[menu_num]['functions'])
#
#
#menu_1 = {
#    'labels': ["Next", "Help", "Exit"],
#    'functions': [_next, _help, _exit]
#}
#menu_2 = {
#    'labels': ["Next", "Back"],
#    'functions': [_next, _back]
#}
#menu_3 = {
#    'labels': ["Back", "Credits"],
#    'functions': [_back, _credits]
#}
#menu_num = 0
#menus = [menu_1, menu_2, menu_3]
#
#
#menu = Menu(menus[menu_num]['labels'], menus[menu_num]['functions'])