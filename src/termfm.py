import subprocess, sys, shutil, os
from art import text2art

from prompt_toolkit import Application
from prompt_toolkit.layout import WindowAlign
from prompt_toolkit.widgets import MenuContainer, TextArea
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import MenuContainer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app

from utils import get_menu_selection, get_folder_from_path, get_dirpath_from_filepath
from menu_data import data, menu_data, recurse


kb = KeyBindings()  # Global keybindings
menu_kb = KeyBindings()  # Keybindings for menu only

heading = text2art("TERMFM", font="cyberlarge")

menu_container = Window(style="fg:ansiwhite bg:ansiblack")
menu = MenuContainer(body=menu_container, menu_items=menu_data, key_bindings=menu_kb)
menu_env = VSplit([menu])

prompt_field = Window(
    dont_extend_height=True,
    content=FormattedTextControl(focusable=False),
    style="bg:ansigray fg:ansiblack",
)


user_input_field_operation_data = []

def user_input_field_handler(buffer):
    input_text = buffer.document.text
    operation = user_input_field_operation_data[0]
    operate_on = user_input_field_operation_data[1]
    menu_focus = user_input_field_operation_data[2]
    retry = False

    if operation == "rename":
        new_path = get_dirpath_from_filepath(operate_on['path'])
        os.rename(operate_on['path'], new_path)

    elif operation == "delete":
        if input_text in ['y', 'Y']:
            if operate_on['type'] == "file":
                os.remove(operate_on['path'])
            elif operate_on['type'] == "folder":
                shutil.rmtree(operate_on['path'])
        elif input_text in ['n', 'N']:
            pass
        else:
            retry = True

    elif operation == "new-file":
        filepath = os.path.join(user_input_field_operation_data[1], input_text)
        with open(filepath, 'w') as fp:
            pass

    elif operation == "new-dir":
        dirpath = os.path.join(user_input_field_operation_data[1], input_text)
        os.mkdir(dirpath)

    if retry == False:
        refresh_menu()
        get_app().layout.focus(menu)
        menu_focus.pop(-1)
        menu.selected_menu = menu_focus
        user_input_field_operation_data.clear()
        prompt_field.content.text = ""
        return False
    else:
        get_app().layout.focus(user_input_field)
        return True

user_input_field = TextArea(
    multiline=False,
    focusable=True,
    dont_extend_height=True,
    style="bg:ansigray fg:ansiblack",
    accept_handler=user_input_field_handler
)


root_container = HSplit(
    [
        Window(
            dont_extend_height=True,
            align=WindowAlign.CENTER,
            style="fg:ansiwhite bg:ansiblack",
            content=FormattedTextControl(text=heading, focusable=False),
        ),
        menu_env,
        prompt_field,
        user_input_field,
    ]
)


layout = Layout(root_container, focused_element=menu)


clipboard = []

def refresh_menu():
    global data
    data = list(os.walk(os.getcwd()))
    menu_data = recurse(data, 0)[0]
    menu.menu_items=menu_data
    menu_env.reset()


# ----------------------------------  KEYBINDINGS  -----------------------------


@kb.add("c-q")
# Exit
def exit_(event):
    event.app.exit()


# KEYBINDINGS FOR MENU


@menu_kb.add("o")
# open a file with its associated program
def start_file(event):
    selection = get_menu_selection(data, menu.selected_menu)
    if selection["type"] == "file":
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, selection["path"]])
    else:
        pass


@menu_kb.add("r")
# rename a file or folder
def rename(event):
    selection = get_menu_selection(data, menu.selected_menu)
    user_input_field_operation_data.append("rename")
    user_input_field_operation_data.append(selection)
    user_input_field_operation_data.append(menu.selected_menu)
    prompt_field.content.text = f"Enter new name for {selection['name']}:"
    get_app().layout.focus(user_input_field)


@menu_kb.add("d")
# delete a file or folder
def delete(event):
    selection = get_menu_selection(data, menu.selected_menu)
    user_input_field_operation_data.append("delete")
    user_input_field_operation_data.append(selection)
    user_input_field_operation_data.append(menu.selected_menu)
    prompt_field.content.text = f"Are you sure you want to delete {selection['name']}? (y/n):"
    get_app().layout.focus(user_input_field)


@menu_kb.add("n", "<any>")
# create a new file or folder
def create_new(event):
    selection = get_menu_selection(data, menu.selected_menu)
    
    if event.key_sequence[1].key == 'f':
        user_input_field_operation_data.append("new-file")
        n_type = "file"
    elif event.key_sequence[1].key == 'd':
        user_input_field_operation_data.append("new-dir")
        n_type = "directory"
    else:
        return

    if selection['type'] == "folder":
        user_input_field_operation_data.append(selection['path'])
    elif selection['type'] == "file":
        dir_path = get_dirpath_from_filepath(selection['path'])
        user_input_field_operation_data.append(dir_path)

    prompt_field.content.text = f"Enter name of the new {n_type}:"
    user_input_field_operation_data.append(menu.selected_menu)
    get_app().layout.focus(user_input_field)


@menu_kb.add("c")
# copy a file or folder
def copy(event):
    clipboard.clear()
    clipboard.append("c")
    clipboard.append(get_menu_selection(data, menu.selected_menu)["path"])


@menu_kb.add("x")
# cut (to move) a file or folder
def cut(event):
    clipboard.clear()
    clipboard.append("x")
    clipboard.append(get_menu_selection(data, menu.selected_menu)["path"])


@menu_kb.add("v")
# paste
def paste(event):
    if len(clipboard) == 0:
        return

    clipboard.append(get_menu_selection(data, menu.selected_menu)["name"])
    src = clipboard[1]
    current_position = get_menu_selection(data, menu.selected_menu)
    dest = ""

    if current_position["type"] == "file":
        dest = get_dirpath_from_filepath(current_position["path"])
    elif current_position["type"] == "folder":
        dest = get_menu_selection(data, menu.selected_menu)["path"]

    if clipboard[0] == "c":
        if os.path.isfile(src) and os.path.isdir(dest):
            shutil.copy2(src, dest)
        if os.path.isdir(src) and os.path.isdir(dest):
            to_add = "/" + get_folder_from_path(src)
            dest += to_add
            shutil.copytree(src, dest)
    elif clipboard[0] == "x":
        if os.path.isfile(src) and os.path.isdir(dest):
            shutil.move(src, dest)
        if os.path.isdir(src) and os.path.isdir(dest):
            to_add = "/" + get_folder_from_path(src)
            dest += to_add
            shutil.move(src, dest)

    clipboard.clear()
    refresh_menu()
    
    
app = Application(key_bindings=kb, layout=layout, full_screen=True,refresh_interval=5)
app.run()

