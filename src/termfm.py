from prompt_toolkit import Application
from prompt_toolkit.layout import WindowAlign
from prompt_toolkit.widgets import MenuContainer, TextArea
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import MenuContainer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app


import subprocess, sys, shutil, os
from art import text2art
from utils import get_input, get_menu_selection, get_folder_from_path
from dir_data import data, menu_data, recurse


kb = KeyBindings()
menu_kb = KeyBindings()

heading = text2art("TERMFM", font="cyberlarge")

menu_container = Window(style="fg:ansiwhite bg:ansiblack")
menu = MenuContainer(body=menu_container, menu_items=menu_data, key_bindings=menu_kb)
menu_env = VSplit([menu])

prompt_field = Window(dont_extend_height=True, content=FormattedTextControl(focusable=False), style="bg:ansigray fg:ansiblack")
user_input_field = TextArea(multiline=False, focusable=True, dont_extend_height=True, style="bg:ansigray fg:ansiblack",
accept_handler=get_input)

root_container =  HSplit([
    Window(dont_extend_height=True, align=WindowAlign.CENTER, style="fg:ansiwhite bg:ansiblack", content=FormattedTextControl(text=heading, focusable=False)),
    menu_env,
    prompt_field,
    user_input_field,
])

layout = Layout(root_container, focused_element=menu)

# -------------------------------  KEYBINDINGS  --------------------------


# Exit
@kb.add('c-q')
def exit_(event):
    event.app.exit()


# KEYBINDINGS FOR MENU

@menu_kb.add('o')
# open a file with its associated program
def start_file(event):
    selection = get_menu_selection(data, menu.selected_menu)
    if selection['type'] == "file":
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, selection['path']])
    else:
        pass


#@menu_kb.add('d')
# delete a file
#def delete_file(event):
#    get_app().layout.focus(user_input_field)

file_clipboard=[]

@menu_kb.add('r')
def rename(event):
    get_menu_selection(data, menu.selected_menu)

#@kb.add('r')
#def rename(event):
    #print(get_menu_selection_path(data, menu.selected_menu))
    
@kb.add('c')
def copy(event):
    file_clipboard.append('c')
    file_clipboard.append(get_menu_selection(data,menu.selected_menu)['path'])
    
@kb.add('x')
def cut(event):
    file_clipboard.append('x')
    file_clipboard.append(get_menu_selection(data,menu.selected_menu)['path'])

@kb.add('v')
def paste(event):
    if(len(file_clipboard)==0):
    	return
    global data
    global menu_data, menu_container, menu, menu_env
    file_clipboard.append(get_menu_selection(data,menu.selected_menu)['name'])
    src=file_clipboard[1]
    current_position=get_menu_selection(data,menu.selected_menu)
    if current_position['type']=='file':
        _dest=current_position['path'].split('/')
        _dest.pop(-1)
        dest='/'.join(_dest)
    elif current_position['type']=='folder':
        dest=get_menu_selection(data,menu.selected_menu)['path']
    if(file_clipboard[0]=='c'):
        if(os.path.isfile(src) and os.path.isdir(dest)):
            shutil.copy2(src,dest)
        if(os.path.isdir(src) and os.path.isdir(dest)):
            to_add='/'+get_folder_from_path(src)
            dest+=to_add
            shutil.copytree(src,dest)
    elif (file_clipboard[0]=='x'):
        if(os.path.isfile(src) and os.path.isdir(dest)):
            shutil.move(src,dest)
        if(os.path.isdir(src) and os.path.isdir(dest)):
            to_add='/'+get_folder_from_path(src)
            dest+=to_add
            shutil.move(src,dest)
    file_clipboard.clear()
    data = list(os.walk(os.getcwd()))
    menu_data = recurse(data,0)[0]
    menu = MenuContainer(body=menu_container, menu_items=menu_data)
    menu_env.reset()
    app.invalidate()
    

@kb.add('d')
def delete(event):
    src=get_menu_selection_path(data, menu.selected_menu)
    if(os.path.isfile(src)):
        os.remove(src)
    else:
        shutil.rmtree(src)  

app = Application(key_bindings=kb, layout=layout, full_screen=True)
app.run()
