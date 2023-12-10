import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication
import serial
from PyQt5.QtCore import QTimer

arduino_port = '/dev/cu.usbserial-110'
baud_rate = 9600

# Variable global para almacenar el sentido
sentido = ""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        grid_layout = QGridLayout()

        self.label_velocidad = QLabel('Velocidad:')
        self.textbox_velocidad = QLineEdit(self)
        self.textbox_velocidad.textChanged.connect(lambda: self.validar_numeros(self.textbox_velocidad))

        self.label_pulsos = QLabel('Pulsos:')
        self.textbox_pulsos = QLineEdit(self)
        self.textbox_pulsos.textChanged.connect(lambda: self.validar_numeros(self.textbox_pulsos))

        self.button_izquierdo = QPushButton('Izquierdo', self)
        self.button_izquierdo.clicked.connect(lambda: self.imprimir_y_enviar('Izquierdo'))

        self.button_derecho = QPushButton('Derecho', self)
        self.button_derecho.clicked.connect(lambda: self.imprimir_y_enviar('Derecho'))

        self.button_enviar = QPushButton('Enviar', self)
        self.button_enviar.clicked.connect(self.enviar_dato)

        # Agregar widgets al diseño de la cuadrícula
        grid_layout.addWidget(self.label_velocidad, 0, 0)
        grid_layout.addWidget(self.textbox_velocidad, 0, 1)

        grid_layout.addWidget(self.label_pulsos, 0, 2)
        grid_layout.addWidget(self.textbox_pulsos, 0, 3)

        grid_layout.addWidget(self.button_izquierdo, 0, 4)
        grid_layout.addWidget(self.button_derecho, 0, 5)

        grid_layout.addWidget(self.button_enviar, 0, 6)

        # Agregar el diseño de la cuadrícula al diseño principal
        layout.addLayout(grid_layout)

        self.setLayout(layout)

        self.setWindowTitle('Control de Robot')
        self.setGeometry(300, 300, 800, 100)

        # Configuración de la comunicación serial
        self.ser = serial.Serial(arduino_port, baud_rate, timeout=1)

        # Configurar un temporizador para verificar los datos recibidos cada 100 ms
        timer = QTimer(self)
        timer.timeout.connect(self.mostrar_dato_recibido)
        timer.start(100)

    def imprimir_y_enviar(self, direccion):
        global sentido  # Acceder a la variable global
        

        if direccion == 'Izquierdo':
            sentido = 0
        else:
            sentido = 1

        print(f'Clic en botón {direccion}')
        print(f'Sentido: {sentido}')

    def enviar_dato(self):
        velocidad = self.textbox_velocidad.text()
        pulsos = self.textbox_pulsos.text()

        # Verificar si los cuadros de texto no están vacíos
        if velocidad and pulsos:
            # Usa un separador reconocible, como ","
            dato = f'{velocidad},{pulsos},{sentido}\n'
            print(f'Enviando datos: {dato}')
            self.ser.write(dato.encode())
        else:
            print("Los campos de velocidad y pulsos no pueden estar vacíos.")

    def mostrar_dato_recibido(self):
        if self.ser.in_waiting > 0:
            received_data = self.ser.readline().decode().strip()
            print(received_data)

    def validar_numeros(self, textbox):
        # Filtrar caracteres no numéricos
        texto = textbox.text()
        nuevo_texto = ''.join(c for c in texto if c.isdigit())
        if texto != nuevo_texto:
            textbox.setText(nuevo_texto)
            textbox.setCursorPosition(len(nuevo_texto))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
