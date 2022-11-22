import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class Suscriptor_Arduino(Node):
    
    def __init__(self): 
        super().__init__('Suscriptor_Arduino')
        self.subscription = self.create_subscription(
            String,
            'sensores_lecturas',
            self.listener_callback,
            10)
        self.subscription

    
    def listener_callback(self, msg):
        self.get_logger().info('Las mediciones son "%s"' % msg.data)

    
def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Suscriptor_Arduino()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()