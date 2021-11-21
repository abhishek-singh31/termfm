from prompt_toolkit import Application
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings


# ------------ KEYBINDINGS: MAKE SEPARATE FILE --------------

kb = KeyBindings()


@kb.add('c-q')
def exit_(event):
    event.app.exit()

# -----------------------------------------------------



root_container =  Window(content=FormattedTextControl(text='Hello world'))

layout = Layout(root_container)

app = Application(key_bindings=kb, layout=layout, full_screen=True)
app.run()
