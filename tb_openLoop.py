##-----------------------------------------------------------------------------##
## ROS2 - PUBLISHER ##
import rclpy
from rclpy.node import Node
from rclpy.clock import Clock

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class Turtlebot3(Node):

    def __init__(self):
        super().__init__('tb_openLoop')

        # Subscriber node to retrieve position.x of Turtlebot3
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',  # Replace with your actual odometry topic
            self.listener_callback,
            10
        )
        self.subscription # prevent unused variable warning

        # Publisher to publish velocity data Trurtlebot3 (Topic: /cmd_vel)
        self.vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        # timer_period = 0.1  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

        # Distance and Time Information
        #Receiveing the user's input
        self.get_logger().info("Press 'cntrl+C' to exit.")
        self.get_logger().info("Let's move your robot!")
        # speed = float(input("Input your speed (0-1m/s): "))
        # distance = float(input("Type your distance (1-5m): "))
        self.distance = 1 # in meters
        self.time = 10 # in seconds
        self.speed = self.distance/self.time # in m/s
        self.reached = False
        # Initial Time(to) and Distance(s0)
        self.t0 = Clock().now().seconds_nanoseconds()[0]
        self.s0 = 0

        # For Scenario #2
        self.speed_max = 1/9 # in m/s
        self.acc = self.speed_max/1 # in m/s^2

        

    def vel_publisher(self, vel = 0.0):
        # Velocity message to publish to the Turtlebot3
        vel_msg = Twist()

        #Since we are moving just in x-axis
        vel_msg.linear.x = vel
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0

        # Publish message
        self.vel_pub.publish(vel_msg)

    # Listener callback from /odom subscription
    def listener_callback(self, msg):
        # Scenario #1
        t1 = Clock().now().seconds_nanoseconds()[0]
        t = t1-self.t0
        if not self.reached:
            X = msg.pose.pose.position.x
            if X < self.distance:
                self.vel_publisher(self.speed)
                self.get_logger().info(f'x position: {X}')
            else:
                self.vel_publisher()
                self.reached = True
                self.get_logger().info('Destination Arrived!')
                self.get_logger().info(f'Distance travelled: {X-self.s0}m, Time taken: {t}s.')

        # # Scenario #2
        # t1 = Clock().now().seconds_nanoseconds()[0]
        # t = t1-self.t0
        # if not self.reached:
        #     X = msg.pose.pose.position.x
        #     if X < self.distance:
        #         vel = 0.0
        #         # Accelerate (acc) for 1 sec
        #         if t <= 1:
        #             vel = self.acc*t
        #         # Constant speed (speed_max) for 8 secs
        #         elif (t > 1) and (t <= 9):
        #             vel = self.speed_max
        #         # Deccelerate (-acc) for 1 sec
        #         elif (t > 9) and (t <= 10):
        #             vel = self.acc*(10-t)
        #         self.vel_publisher(vel)
        #         self.get_logger().info(f'x position: {X}')
                
        #     else:
        #         self.vel_publisher()
        #         self.reached = True
        #         self.get_logger().info('Destination Arrived!')
        #         self.get_logger().info(f'Distance travelled: {X-self.s0}m, Time taken: {t}s.')

                

def main(args=None):
    rclpy.init(args=args)
    tb_openLoop = Turtlebot3()
    rclpy.spin(tb_openLoop)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tb_openLoop.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
##-----------------------------------------------------------------------------##