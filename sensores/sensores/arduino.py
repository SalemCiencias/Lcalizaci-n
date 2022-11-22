#!/usr/bin/env python
# license removed for brevity
import rclpy
from rclpy.node import Node
import serial
import threading

from std_msgs.msg import String

class ArduinoPublisher(Node):
    
    def __init__(self):

        #Argumentos para crear el nodo y el topic con el cual se comunica.
        super().__init__('arduino_publisher')
    
        #Argumentos que crean la lectura del puerto serial.
        self.port = serial.Serial('/dev/ttyACM0',9600,timeout=1)
        self.port.reset_input_buffer()

        #Diccionario de sensores.
        self.sensores = {}

        self.publisher_ = self.create_publisher( String, 'sensores_lecturas', 10) 
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info("init")

    def read_sensor_package(self,bytes_serial):
        """
        Función que lee los mensajes de nuestro arduino.

        Parametros
        ------------
        bytes_serial: Un mensaje de algún sensor.

        Return
        ----------------
        sensor_index: El sensor al cual pertenece la lectura.
        reading: La distancia en centimetros.
        """

        if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:  # check for 'YY'
            # print(bytes_serial)
            sensor_index = bytes_serial[2]
            reading = bytes_serial[3]+bytes_serial[4]
            return sensor_index, reading
        else:
            return -1, 0
    
    def timer_callback(self):
        """
        Función que leera del puerto serial conectado al arduino y recibirá la información.

        Parametros
        -------------
        serial: El puerto al cuál debe acceder.
        sensores: Un diccionario que contendrá los sensores.
        """
        sensor_index = 0
        sensor_reading = 0

        contador = self.port.in_waiting
        bytes_to_read = 5   

        if contador > bytes_to_read - 1:
            
            bytes_serial = self.port.read(bytes_to_read)

            sensor_index, sensor_reading = self.read_sensor_package(bytes_serial)

        if sensor_index >= 0:
            if sensor_index not in self.sensores:
                self.sensores[sensor_index] = 0
            if sensor_reading > 0:
                self.sensores[sensor_index]=sensor_reading
                msg = String()
                msg.data = str(self.sensores)
                self.publisher_.publish(msg)
                #print(self.sensores)
            
def main(args=None):
    rclpy.init(args=args)

    arduino_publisher = ArduinoPublisher()

    rclpy.spin(arduino_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


