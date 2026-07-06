## Core Architectural Layers
1. The Orchestrator / Entry Point (main.py)
Role: Sets up the system on boot.
Mechanism: Spawns a background worker thread (threading.Thread) dedicated exclusively to running rclpy.spin(). This prevents the GUI window from lagging or locking up when ROS 2 sends or receives navigation messages. It then launches the primary PyQt5 window on the main thread.

3. The UI View Layer (main_window.py)
Role: Visual presentation and user interaction.
Mechanism: Builds the layout, input fields, and buttons. When a user interacts with the panel (e.g., clicking "Add Waypoint"), it extracts the raw text coordinates, appends them to a local cache tracking array, and fires an internal signaling callback to pass that data downstream.

5. The Input Guard Layer (validators.py)
Role: Data filtering and application safety.
Mechanism: Attaches restrictive validation filters directly to text field nodes. It blocks alphabetic characters or symbols at the hardware keystroke level, ensuring the program never encounters ValueError type casting crashes.

6. The Robotic Client Layer (nav2_client.py)
Role: Handles ROS 2 middleware lifecycle events.
Mechanism: Houses the Action Client that connects to the /navigate_to_pose channel. It converts the sequential numeric array sent from the UI into a series of structured MapsToPose.Goal messages. It manages the index tracking system internally, advancing forward only when target completion feedback is validated.

## Execution Flow Blueprint
Input: User types coordinates \rightarrow validators.py filters input safely.
Submission: Click "Add Waypoint" \rightarrow main_window.py fires a callback event.
Bridge: main.py intercepts the callback event and relays the coordinate array data across thread boundaries to the ROS node.
Action: nav2_client.py formats a goal message, contacts the Nav2 action server, monitors live distance feedback, and automatically increments the index tracking pointer upon successful arrival to push the next waypoint..
