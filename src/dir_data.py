# RENAME FILE TO MENU_DATA


from prompt_toolkit.widgets import MenuItem
import os

from utils import print_dir, print_file


# walk the current dir and get its contents
data = list(os.walk(os.getcwd()))


def recurse(_data, index):
    output = []
    children = []
    sum = 0

    dir_name = _data[index][0].split("/")[-1]
    menu_item = MenuItem(text=print_dir(dir_name))

    output.append(menu_item)

    if len(_data[index][1]) == 0:
        children = []

    else:
        for i in range(len(_data[index][1])):
            rec = recurse(_data, index + sum + 1)
            sum += rec[1] + 1
            children += rec[0]

    remaining_files = _data[index][2]
    for i in range(len(remaining_files)):
        children.append(MenuItem(text=print_file(remaining_files[i])))

    menu_item.children = children

    return [output, len(_data[index][1])]


menu_data = recurse(data, 0)[0]
