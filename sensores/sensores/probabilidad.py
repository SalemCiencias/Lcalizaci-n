import rclpy
from rclpy.node import Node
import numpy as np
import time
import math

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
        self.time_al = time.perf_counter()

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

        #Nuestras matrices relevantes para la distribución de proba y la media.
        new_arr = np.array([[[307,40,51,0,145,22],[53,50,190,96,21,0],[45,188,172,22,0,0],[125,176,120,0,0,50],[164,20,26,0,0,46],[92,22,0,0,49,97],[17,20,0,52,256,163],[84,0,55,192,100,20]],[[50,155,130,100,89,157],[72,100,158,108,0,0],[76,150,0,167,47,0],[110,0,0,90,0,86],[50,0,0,0,154,111],[103,0,0,138,95,155],[60,93,0,47,123,192],[59,0,100,145,177,0]],[[46,0,169,104,157,200],[96,142,212,125,125,80],[130,232,153,240,115,46],[175,100,172,121,46,215],[64,177,146,45,200,142],[72,350,87,100,147,213],[107,80,81,145,225,145],[65,81,162,214,100,183]]])
        self.medias = new_arr.reshape(3,8,6)
        self.dist = np.zeros((3,8,6))

        ##Asigna la misma probabilidad a todas las mediciones
        prob = 1 / 144
        for index1 in range(3):
            for index2 in range(8):
                for index3 in range(6):
                    self.dist[index1][index2][index3] = prob

        #La información de dónde está nuestro robot.
        self.a = 0.0
        self.b = 0.0

        self.aux = 0

    def pub_locate(self):
        """
        Función que publicará los mensajes obtenidos de la probabilidad.

        Parameters
        -----------
        msg: String.
        Nuestra información a publicar.

        Return
        -----------
        None.

        """
        if self.aux == 100:
            self.calculo_Propabilidad()
            self.aux = 0
        ms = String()
        ms.data = "({},{})".format(self.a,self.b)
        self.publisher_.publish(ms)
        print(ms.data)
        self.aux += 1

    def normaliza(self,constante):
        """
        Función que normaliza nuestra creencia, solo le pasamos la constante.

        Parameters
        -----------
        constante: int.
        Constante que utilizamos en nuestros calculos.

        Return
        ----------
        None
        """  
        for index1 in range(3):
            for index2 in range(8):
                for index3 in range(6):
                    self.dist[index1][index2][index3] = pow(constante, -1) * self.dist[index1][index2][index3]
    
    def proba_inicial(self,constante):
        """
        Función que calcula la proba de que el robot esté en cualquier casilla al principio.

        Parameters
        -----------
        constante:float.
        Una variable auxiliar.
        """
        for index1 in range(3):
            for index2 in range(8):
                for index3 in range(6):
                    self.dist[index1][index2][index3] = ((1 / (math.sqrt(2 * math.pi) * 9.81)) * pow(math.e, (- pow(self.lecturas[index3]- self.medias[index1][index2][index3],2)) / 2* pow(9.81, 2))) * self.dist[index1][index2][index3]
                    constante = constante + self.dist[index1][index2][index3]
        return constante
        

    def calculo_Probabilidad(self):
        """
        Función que resuelve el problema de dónde se encuentra nuestro robot dadas las mediciones de nuestros sensores.

        Parameters
        ------------
        None.

        Return
        ------------
        None.

        """


        ##Calcula la probabilidad de que el robot este en todas las posibles posiciones 
        constante = 0.0
        for index1 in range(3):
            for index2 in range(8):
                for index3 in range(6):
                    self.dist[index1][index2][index3] = ((1 / (math.sqrt(2 * math.pi) * 9.81)) * pow(math.e, (- pow(self.lecturas[index3]- self.medias[index1][index2][index3],2)) / 2* pow(9.81, 2))) * self.dist[index1][index2][index3]
                    constante = constante + self.dist[index1][index2][index3]   

        #self.proba_inicial(0.0)

        self.normaliza(constante)

        ##Se calcula la probabilidad para las 8 posibles rotaciones de cada celda multiplicando la probabilidad de cada sonar 
        arr_prob_celdas = np.zeros((3,8))
        for index1 in range(3):
            for index2 in range(8):
                proba = 1
                for index3 in range(6):
                    proba = proba * self.dist[index1][index2][index3]
                
                arr_prob_celdas[index1][index2] = proba

        ##Se encuentra la posicion de mayor probabilidad
        contador1_indice = 0.0
        contador2_indice = 0.0 
        contador = 0.0
        for index1 in range(3):
            for index2 in range(8):
                if contador <= arr_prob_celdas[index1][index2]:
                    contador1_indice = index1
                    contador2_indice = index2
                    contador = arr_prob_celdas[index1][index2]
                        
        ##Aqui el da el valor a la información para ser publicada por el topic.
        self.a = contador1_indice
        self.b = contador2_indice 

        self.pub_locate()     
    
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
        #self.get_logger().info('Las mediciones son "%s"' % msg.data)

        timer2 = time.perf_counter()
        if timer2-self.time_al > 10:
            self.crea_lista(msg.data)
            self.timer = time.perf_counter()

    def listener_odom(self):
        """
        Función que procesa los mensajes publicados por el odometro del robot.

        Parameters
        -----------
        None

        Return
        -----------
        None
        """
        self.get_logger().info("Odometro")
        
    
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