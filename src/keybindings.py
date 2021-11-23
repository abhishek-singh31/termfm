from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.data_structures import Point


kb = KeyBindings()
cursor = {'x': 0, 'y': 0}

# Exit
@kb.add('c-q')
def exit_(event):
    event.app.exit()


def movecursor_down():
    cursor['x'] += 1
    return Point(cursor['x'], cursor['y'])

# down arrow
@kb.add('down')
def menu_down(event):
    # print(event.app.layout.current_control)
    event.app.layout.current_control.get_cursor_position = movecursor_down
    



# down arrow
