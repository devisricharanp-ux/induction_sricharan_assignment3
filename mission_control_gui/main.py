import sys
import threading

import rclpy

from .gui.nav2_client import MissionClient
from .gui.main_window import build_gui


def main():
    rclpy.init()
    node = MissionClient()

    # Spin ROS in a background thread so it never blocks the Qt event loop.
    # This is what previously made you unable to add a new waypoint until
    # the old mission finished: rclpy.spin() was running on the same thread
    # as the GUI.
    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    app, window = build_gui(node)
    try:
        exit_code = app.exec_()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
