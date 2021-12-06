from prompt_toolkit.widgets import MenuContainer
from prompt_toolkit.layout.containers import Window
from keybindings import kb
from dir_data import data, menu_data
from utils import get_menu_selection_path,find
import shutil
import os
menu_container = Window(style="fg:ansiwhite bg:ansiblack")

menu = MenuContainer(body=menu_container, menu_items=menu_data)



copy_paste=[]
cut_paste=[]

def modify(src):
    k=0
    i=len(src)-1
    while(src[i]!='/'):
        i=i-1
        k=k+1
    return src[-k:]

@kb.add('r')
def rename(event):
    print(get_menu_selection_path(data, menu.selected_menu))
    
@kb.add('c')
def copy(event):
    copy_paste.append(get_menu_selection_path(data, menu.selected_menu))
    
@kb.add('m')
def cut(event):
    cut_paste.append(get_menu_selection_path(data, menu.selected_menu))

@kb.add('v')
def copy_paste_fun(event):
    copy_paste.append(get_menu_selection_path(data, menu.selected_menu))
    src=copy_paste[0]
    dest=copy_paste[1]
    if(os.path.isfile(src) and os.path.isdir(dest)):
        shutil.copy2(src,dest)
    if(os.path.isdir(src) and os.path.isdir(dest)):
        to_add='/'+modify(src)
        dest+=to_add
        shutil.copytree(src,dest)
    copy_paste.clear()
    
@kb.add('x')
def cut_paste_fun(event):
    cut_paste.append(get_menu_selection_path(data, menu.selected_menu))
    src=cut_paste[0]
    dest=cut_paste[1]
    if(os.path.isfile(src) and os.path.isdir(dest)):
        shutil.move(src,dest)
    if(os.path.isdir(src) and os.path.isdir(dest)):
        to_add='/'+modify(src)
        dest+=to_add
        shutil.move(src,dest)
    cut_paste.clear()
    
@kb.add('d')
def delete(event):
    src=get_menu_selection_path(data, menu.selected_menu)
    if(os.path.isfile(src)):
        os.remove(src)
    else:
        shutil.rmtree(src)
    reset()
    
