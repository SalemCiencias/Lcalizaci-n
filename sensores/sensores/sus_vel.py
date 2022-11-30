import rclpy
from rclpy.node import Node

class Suscriptor_CMD(Node):
    
    def __init__(self):
        super().__init__('Suscriptor_Arduino')
        self.subscription = self.create_subscription(
            String,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self):
        pass

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Suscriptor_CMD()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()