from pynput import mouse
from PyQt5.QtWidgets import QApplication

class ClickDetector:
    """
    A class to detect mouse clicks and determine if they are within a selected monitor's area.

    Attributes:
        left_click_coordinates (tuple): Coordinates of the last detected left click.
        listener (mouse.Listener): Listener object for detecting mouse events.
        selected_monitor (dict): Information about the currently selected monitor.
    """

    def __init__(self):
        """
        Initializes the ClickDetector class and starts the mouse listener.
        """
        self.left_click_coordinates = None
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()
        self.selected_monitor = None

    def on_click(self, x, y, button, pressed):
        """
        Event handler for mouse clicks. Records the coordinates if the left button is pressed.

        Args:
            x (int): The x-coordinate of the mouse click.
            y (int): The y-coordinate of the mouse click.
            button (mouse.Button): The mouse button that was clicked.
            pressed (bool): Whether the button was pressed.
        """
        if button == mouse.Button.left and pressed:
            self.left_click_coordinates = (x, y)
            print(f"Left click detected at ({x}, {y})")

    def has_left_clicked(self):
        """
        Checks if a left click has been recorded.

        Returns:
            bool: True if a left click has been recorded, False otherwise.
        """
        return self.left_click_coordinates is not None

    def stop(self):
        self.listener.stop()

    @staticmethod
    def get_info_monitors():
        """
        Retrieves information about all connected monitors.

        Returns:
            list: A list of dictionaries containing information about each monitor.
        """
        app = QApplication([])
        monitors = []
        for screen in app.screens():
            geometry = screen.geometry()
            monitors.append({
                'name': screen.name(),
                'width': geometry.width(),
                'height': geometry.height(),
                'x': geometry.left(),
                'y': geometry.top(),
                'right': geometry.right(),
                'bottom': geometry.bottom(),
                'is_primary': screen == app.primaryScreen(),
            })
        QApplication.quit()
        for monitor in monitors:
            print(f"Monitor: {monitor}")
        return monitors

    def select_monitor(self, index):
        """
        Selects a monitor based on its index in the list of monitors.

        Args:
            index (int): The index of the monitor to select.
        """
        monitors = self.get_info_monitors()
        if 0 <= index < len(monitors):
            self.selected_monitor = monitors[index]
            print(f"Selected Monitor {index}: {self.selected_monitor}")
        else:
            print(f"Invalid monitor index: {index}")

    def is_click_in_selected_monitor(self):
        """
        Checks if the recorded left click is within the selected monitor's area.

        Returns:
            bool: True if the left click is within the selected monitor's area, False otherwise.
        """
        if self.selected_monitor and self.left_click_coordinates:
            x, y = self.left_click_coordinates
            return (self.selected_monitor["x"] <= x < self.selected_monitor["right"]) and (self.selected_monitor["y"] <= y < self.selected_monitor["bottom"])
        return False
    
    def approximate_pause_click_in_monitor(self):
        """
        Checks if the recorded left click is within the pause button area of the selected monitor.
        The approximation is based on a fixed percentage of the monitor's height.

        Returns:
            bool: True if the left click is within the pause button area, False otherwise.
        """
        approximation_percentage_click_to_pause = 0.9240
        if self.is_click_in_selected_monitor():
            height_to_click = self.selected_monitor["height"] * approximation_percentage_click_to_pause
            return True if self.left_click_coordinates[1] <= (self.selected_monitor["y"] + height_to_click) else False
        return False