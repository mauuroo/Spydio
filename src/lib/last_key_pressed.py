import keyboard

#Global variable to store the last key pressed.
last_key = None

def on_key_event(event):
    """
    Updates the global `last_key` variable with the name of the key that was pressed.

    Args:
        event (keyboard.KeyboardEvent): The event object containing information about the key press.
    """
    global last_key
    last_key = event.name

def get_last_key():
    """
    Configures the event handler for key presses and returns the last key pressed.

    Returns:
        str: The name of the last key pressed as recorded in the global `last_key` variable.
    """
    keyboard.on_press(on_key_event)
    return last_key