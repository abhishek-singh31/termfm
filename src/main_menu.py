from prompt_toolkit.widgets import MenuContainer
from prompt_toolkit.layout.containers import Window

from keybindings import kb
from dir_data import data, menu_data
from utils import get_menu_selection_path

menu_container = Window(style="fg:ansiwhite bg:ansiblack")

menu = MenuContainer(body=menu_container, menu_items=menu_data)






@kb.add('o')
def start_file(event):
    print("hehe")




@kb.add('r')
def rename(event):
    get_menu_selection_path(data, menu.selected_menu)

