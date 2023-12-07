import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
import serial
from PyQt5.QtCore import QTimer

arduino_port = '/dev/cu.usbmodem1101'
baud_rate = 9600

# Variable global para almacenar el sentido
sentido = ""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_velocidad = QLabel('Velocidad:')
        self.textbox_velocidad = QLineEdit(self)

        self.label_pulsos = QLabel('Pulsos:')
        self.textbox_pulsos = QLineEdit(self)

        self.button_izquierdo = QPushButton('Izquierdo', self)
        self.button_izquierdo.clicked.connect(lambda: self.imprimir_y_enviar('Izquierdo'))

        self.button_derecho = QPushButton('Derecho', self)
        self.button_derecho.clicked.connect(lambda: self.imprimir_y_enviar('Derecho'))

        self.button_enviar = QPushButton('Enviar', self)
        self.button_enviar.clicked.connect(self.enviar_dato)

        layout.addWidget(self.label_velocidad)
        layout.addWidget(self.textbox_velocidad)

        layout.addWidget(self.label_pulsos)
        layout.addWidget(self.textbox_pulsos)

        layout.addWidget(self.button_izquierdo)
        layout.addWidget(self.button_derecho)

        layout.addWidget(self.button_enviar)

        self.setLayout(layout)

        self.setWindowTitle('Interfaz Arduino')
        self.setGeometry(300, 300, 400, 200)

        # Configuración de la comunicación serial
        self.ser = serial.Serial(arduino_port, baud_rate, timeout=1)

    def imprimir_y_enviar(self, direccion):
        global sentido  # Acceder a la variable global
        sentido = direccion
        print(f'Clic en botón {direccion}')
        # Aquí puedes agregar lógica adicional si es necesario
        # Por ahora, simplemente enviamos los datos al Arduino
        #self.enviar_dato()

    def enviar_dato(self):
        velocidad = self.textbox_velocidad.text()
        pulsos = self.textbox_pulsos.text()

        # Usa un separador reconocible, como ","
        dato = f'{velocidad},{pulsos},{sentido}\n'
        print(f'Enviando datos: {dato}')





        self.ser.write(dato.encode())

    def mostrar_dato_recibido(self):
        if self.ser.in_waiting > 0:
            received_data = self.ser.readline().decode().strip()
            print(received_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    # Configurar un temporizador para verificar los datos recibidos cada 100 ms
    timer = QTimer(mainWindow)
    timer.timeout.connect(mainWindow.mostrar_dato_recibido)
    timer.start(100)

    sys.exit(app.exec_())
