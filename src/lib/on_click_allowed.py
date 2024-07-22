from pynput import mouse

class ClickDetector:
    def __init__(self):
        self.left_click_coordinates = None
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.left_click_coordinates = (x, y)
            print(f"Left click detected at ({x}, {y})")

    def get_last_left_click(self):
        return self.left_click_coordinates

    def has_left_clicked(self):
        return self.left_click_coordinates is not None

    def stop(self):
        self.listener.stop()

