import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import Twist


class MissionClient(Node):
    def __init__(self):
        super().__init__('mission_client')
        self.action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self.waypoints = []
        self.current_waypoint_index = 0
        self.successful_waypoints = 0
        self.goal_handle = None
        self.busy = False  # True while a goal is in flight
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.cmd_vel_publish_  = self.create_publisher(Twist,"/cmd_vel",10)
           

    def send_vel_timer(self):
        msg = Twist()
        msg.linear.x = float(0.0)
        msg.angular.z = float(0.0)
        self.cmd_vel_publish_.publish(msg)      

    def emergency_stop(self):
        self.cmd_vel_pub.publish(Twist())
        self.get_logger().warn("KILL SWITCH BUTTON PRESSED.")
        self.waypoints = []
        self.timer = self.create_timer(0.000025,self.send_vel_timer)
          

    def add_waypoint(self, x, y):
        self.waypoints.append((x, y))
        self.get_logger().info(f"Queued waypoint: x={x}, y={y}")
    # no auto-start here anymore

    def dispatch_mission(self):
        if not self.busy and self.current_waypoint_index < len(self.waypoints):
            self.send_next_waypoint()
        else:
            self.get_logger().warn("Already running, or no waypoints queued.")
     

    def send_next_waypoint(self):
        if self.current_waypoint_index >= len(self.waypoints):
            self.busy = False
            self.get_logger().info("Waiting for more waypoints...")
            return
        

        self.busy = True
        x, y = self.waypoints[self.current_waypoint_index]
        self.get_logger().info(f"Dispatching Waypoint [{self.current_waypoint_index + 1}/{len(self.waypoints)}]: x={x}, y={y}")

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0
        goal_msg.pose.pose.orientation.w = 1.0

        self.action_client.wait_for_server()
        send_goal_future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.goal_handle = future.result()
        if not self.goal_handle.accepted:
            self.get_logger().warn(f"Waypoint {self.current_waypoint_index + 1} was rejected by the server.")
            self.current_waypoint_index += 1
            self.send_next_waypoint()
            return

        self.get_logger().info(f"Waypoint {self.current_waypoint_index + 1} accepted. Tracking progress...")
        get_result_future = self.goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        distance_remaining = feedback_msg.feedback.distance_remaining
        self.get_logger().info(f"Distance remaining: {distance_remaining:.2f} meters")

    def get_result_callback(self, future):
        result = future.result()
        status = result.status

        if status == 4:
            self.get_logger().info(f"Waypoint {self.current_waypoint_index + 1} reached successfully!")
            self.successful_waypoints += 1
        else:
            self.get_logger().warn(f"Waypoint {self.current_waypoint_index + 1} failed or aborted with status: {status}")

        self.current_waypoint_index += 1
        self.send_next_waypoint()
