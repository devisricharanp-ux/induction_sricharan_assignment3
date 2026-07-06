import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, \
    QFormLayout, QPushButton, QHBoxLayout

from .validators import parse_coordinate_pair


def build_gui(mission_client):
    """Builds the Rover Controller window. `mission_client` is the single,
    already-spinning MissionClient node (see main.py)."""

    app = QApplication.instance() or QApplication([])
    window = QWidget()
    layout = QFormLayout()
    x_input = QLineEdit()
    y_input = QLineEdit()

    def waypoint_added():
        coords = parse_coordinate_pair(x_input.text(), y_input.text())
        if coords:
            x_val, y_val = coords
            mission_client.add_waypoint(x_val, y_val)  # queues; doesn't block GUI
            x_input.clear()
            y_input.clear()

    def waypoint_clear():
        x_input.clear()
        y_input.clear()
        
    def dispatch_mission():
        mission_client.dispatch_mission()
    def emergency_kill():
        mission_client.emergency_stop()
    def resume():
        mission_client.resume()    


    layout.setContentsMargins(30, 65, 20, 20)   # <- back to build_gui's level

    window.setWindowTitle("Rover Controller")
    window.setGeometry(100, 100, 650, 300)

    QLabel("Welcome!! ", parent=window).move(20, 15)
    QLabel("Add waypoints below ", window).move(20, 30)

    layout.addRow("X-coordinate:", x_input)
    layout.addRow("Y-coordinate:", y_input)

    btn_add = QPushButton("Add waypoint")
    btn_clear = QPushButton("Clear")
    btn_dispatch = QPushButton("Dispatch")
    btn_emergency = QPushButton("KILL SWITCH")
    btn_resume = QPushButton("Resume")
    
    btn_emergency.setStyleSheet("background-color: red; color: white; font-weight: bold; padding: 8px;")
   

    btn_add.clicked.connect(waypoint_added)
    btn_clear.clicked.connect(waypoint_clear)
    btn_dispatch.clicked.connect(dispatch_mission)
    btn_emergency.clicked.connect(emergency_kill)
   

    button_layout = QHBoxLayout()
    button_layout.addWidget(btn_add)
    button_layout.addWidget(btn_clear)
    button_layout.addWidget(btn_dispatch)
    button_layout.addWidget(btn_emergency)
   
    layout.addRow(button_layout)

    window.setLayout(layout)
    window.show()
    return app, window
