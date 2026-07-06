# mission_control_gui

PyQt5 GUI for queuing and dispatching Nav2 waypoints one at a time.

Run: `python3 main.py`

## Fix note
Waypoints used to be un-addable while a mission was in progress because
`rclpy.spin()` ran on the GUI thread, recreated on every button click.
Now a single `MissionClient` node spins in a background thread; clicking
"Add waypoint" just queues a coordinate via `add_waypoint()`, which is
picked up automatically once the node is free.
