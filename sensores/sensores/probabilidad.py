import rclpy
from rclpy.node import Node
import numpy as np
import time

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

        #Timer para procesar los mensajes recibidos de algunos topicos.
        self.timer = time.perf_counter()

        #Lista para tener nuestras lecturas de sensores en tiempo constante.
        self.lecturas = [0,1,2,3,4,5]


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

        self.medias = np.zeros((3,8,6))
        
    
    def crea_lista(self,msg):
        """
        Función que del mensaje, actualiza nuestra lista para tener las lecturas más recientes de los sensores.

        Parameters
        -----------
        msg: String.
        La cadena con la información de nuestro topic.

        Return
        -----------
        None.
        """      

        contador = 0
        for i in range(len(msg)):
            if msg[i] == ":":
                self.lecturas[contador] = msg[i+2]
                contador += 1


    def listener_sensors(self, msg):
        """
        Función que procesa los mensajes recibidos del topico de sensores.

        Parameters
        ---------
        msg: String
        La cadena con la información'recibida del topic.

        Return
        --------
        None.
        """
        self.get_logger().info('Las mediciones son "%s"' % msg.data)

        timer2 = time.perf_counter()
        if timer2-timer > 10:
            self.crea_lista(msg.data)
            self.timer = time.perf_counter()
        
        


    def listener_odom(self,msg):
        """
        Función que procesará los mensajes obtenidos del odometro.

        Parameters
        -----------
        msg: String.
        Nuestra información del odometro.

        Return
        -----------
        None.

        """
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