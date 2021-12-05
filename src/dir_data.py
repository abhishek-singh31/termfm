# RENAME FILE TO MENU_DATA


from prompt_toolkit.widgets import MenuItem
import os

from utils import print_dir, print_file


# walk the current dir and get its contents
data = list(os.walk(os.getcwd()))



def recurse(index):
    output = []
    children = []
    sum = 0
   
    dir_name = data[index][0].split('/')[-1]
    menu_item = MenuItem(text=print_dir(dir_name))
    
    output.append(menu_item)
    
    if len(data[index][1]) == 0:
        children = []

    else:
        for i in range(len(data[index][1])):
            rec = recurse(index+sum+1)
            sum += rec[1] + 1
            children += rec[0]

    remaining_files = data[index][2]
    for i in range(len(remaining_files)):
        children.append(MenuItem(text=print_file(remaining_files[i]))) 
    
    menu_item.children = children

    return [output, len(data[index][1])]


menu_data = recurse(0)[0]


