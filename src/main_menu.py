from prompt_toolkit.widgets import MenuContainer, MenuItem
from prompt_toolkit.layout.containers import Window

from keybindings import kb
from dir_data import cwd_data

menu_container = Window(style="fg:ansiwhite bg:ansiblack")
# menu = MenuContainer(body=menu_container, menu_items=[MenuItem(text="hello", children=[MenuItem(text="1", children=[MenuItem(text="haha"), MenuItem(text="hehe")]),
                                                                                       # MenuItem(text="2")]), MenuItem(text="world")])

menu = MenuContainer(body=menu_container, menu_items=cwd_data)











@kb.add('r')
def rename(event):
    print(menu.selected_menu)

