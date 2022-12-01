import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class Suscriptor_Arduino(Node):
    
    def __init__(self): 
        super().__init__('Suscriptor_Arduino')

        #Nuestra suscripción al topico de los Sensores.
        self.sub_sensors = self.create_subscription(
            String,
            'sensores_lecturas',
            self.listener_sensors,
            10)
        self.sub_sensors

        #Nuestro topico publisher que da la ubicación del robot.
        self.publisher_ = self.create_publisher( String, 'locate', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.pub_locate)

        #Nuestro otro suscriptor al topic de cmd_vel.
        self.sub_odom = self.create_subscription(
            String,
            'odom',
            self.listener_odom,
            10)
        self.sub_odom

        self.get_logger().info("init")
        

    
    def listener_sensors(self, msg):
        self.get_logger().info('Las mediciones son "%s"' % msg.data)

    def listener_odom(self,msg):
        self.get_logger().info('el odometro')

    def pub_locate(self):
        pass
    
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