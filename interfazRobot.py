import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication
import serial
from PyQt5.QtCore import QTimer

arduino_port = '/dev/cu.usbserial-110'
baud_rate = 9600

# Variable global para almacenar el sentido
sentido = ""

sentido2 = ""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        grid_layout = QGridLayout()


        self.label_modeloD = QLabel('Modelo Directo:')
        self.label_q1 = QLabel('q1:')
        self.textbox_q1 = QLineEdit(self)

        self.label_q2 = QLabel('q2:')
        self.textbox_q2 = QLineEdit(self)

        self.label_q3 = QLabel('q3:')
        self.textbox_q3 = QLineEdit(self)

        self.label_modeloI = QLabel('Modelo Inverso:')
        self.label_x = QLabel('x:')
        self.textbox_x = QLineEdit(self)

        self.label_y = QLabel('y:')
        self.textbox_y = QLineEdit(self)

        self.label_esp = QLabel('                      ')


        self.label_motor1 = QLabel('Motor 1:')
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

        self.label_motor2 = QLabel('Motor 2:')
        self.label_velocidad2 = QLabel('Velocidad:')
        self.textbox_velocidad2 = QLineEdit(self)
        self.textbox_velocidad2.textChanged.connect(lambda: self.validar_numeros2(self.textbox_velocidad2))

        self.label_pulsos2 = QLabel('Pulsos:')
        self.textbox_pulsos2 = QLineEdit(self)
        self.textbox_pulsos2.textChanged.connect(lambda: self.validar_numeros2(self.textbox_pulsos2))

        self.button_izquierdo2 = QPushButton('Izquierdo', self)
        self.button_izquierdo2.clicked.connect(lambda: self.imprimir_y_enviar2('Izquierdo'))

        self.button_derecho2 = QPushButton('Derecho', self)
        self.button_derecho2.clicked.connect(lambda: self.imprimir_y_enviar2('Derecho'))

        self.button_enviar2 = QPushButton('Enviar', self)
        self.button_enviar2.clicked.connect(self.enviar_dato2)

        self.label_motor3 = QLabel('Motor 3:')
        self.label_velocidad3 = QLabel('Velocidad:')
        self.textbox_velocidad3 = QLineEdit(self)
        self.textbox_velocidad3.textChanged.connect(lambda: self.validar_numeros2(self.textbox_velocidad2))

        self.label_pulsos3 = QLabel('Pulsos:')
        self.textbox_pulsos3 = QLineEdit(self)
        self.textbox_pulsos3.textChanged.connect(lambda: self.validar_numeros2(self.textbox_pulsos2))

        self.button_izquierdo3 = QPushButton('Izquierdo', self)
        self.button_izquierdo3.clicked.connect(lambda: self.imprimir_y_enviar2('Izquierdo'))

        self.button_derecho3 = QPushButton('Derecho', self)
        self.button_derecho3.clicked.connect(lambda: self.imprimir_y_enviar2('Derecho'))

        self.button_enviar3 = QPushButton('Enviar', self)
        self.button_enviar3.clicked.connect(self.enviar_dato2)

        # Agregar widgets al diseño de la cuadrícula
        grid_layout.addWidget(self.label_modeloD, 0, 0)
        grid_layout.addWidget(self.label_q1, 1, 0)
        grid_layout.addWidget(self.textbox_q1, 1, 1)
        grid_layout.addWidget(self.label_q2, 2, 0)
        grid_layout.addWidget(self.textbox_q2, 2, 1)
        grid_layout.addWidget(self.label_q3, 3, 0)
        grid_layout.addWidget(self.textbox_q3, 3, 1)

        grid_layout.addWidget(self.label_modeloI, 4, 0)
        grid_layout.addWidget(self.label_x, 5, 0)
        grid_layout.addWidget(self.textbox_x, 5, 1)
        grid_layout.addWidget(self.label_y, 6, 0)
        grid_layout.addWidget(self.textbox_y, 6, 1)

        grid_layout.addWidget(self.label_motor1, 1, 4)
        grid_layout.addWidget(self.label_velocidad, 2, 4)
        grid_layout.addWidget(self.textbox_velocidad, 2, 5)

        grid_layout.addWidget(self.label_pulsos, 2, 6)
        grid_layout.addWidget(self.textbox_pulsos, 2, 7)

        grid_layout.addWidget(self.button_izquierdo, 2, 8)
        grid_layout.addWidget(self.button_derecho, 2, 9)

        grid_layout.addWidget(self.button_enviar, 2, 10)

        grid_layout.addWidget(self.label_motor2, 3, 4)
        grid_layout.addWidget(self.label_velocidad2, 4, 4)
        grid_layout.addWidget(self.textbox_velocidad2, 4, 5)

        grid_layout.addWidget(self.label_pulsos2, 4, 6)
        grid_layout.addWidget(self.textbox_pulsos2, 4, 7)

        grid_layout.addWidget(self.button_izquierdo2, 4, 8)
        grid_layout.addWidget(self.button_derecho2, 4, 9)

        grid_layout.addWidget(self.button_enviar2, 4, 10)


        #Motor 3

        grid_layout.addWidget(self.label_motor3, 5, 4)
        grid_layout.addWidget(self.label_velocidad3, 6, 4)
        grid_layout.addWidget(self.textbox_velocidad3, 6, 5)

        grid_layout.addWidget(self.label_pulsos3, 6, 6)
        grid_layout.addWidget(self.textbox_pulsos3, 6, 7)

        grid_layout.addWidget(self.button_izquierdo3, 6, 8)
        grid_layout.addWidget(self.button_derecho3, 6, 9)

        grid_layout.addWidget(self.button_enviar3, 6, 10)

        grid_layout.addWidget(self.label_esp, 5, 3)

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

    def imprimir_y_enviar2(self, direccion):
        global sentido2  # Acceder a la variable global
        

        if direccion == 'Izquierdo':
            sentido2 = 0
        else:
            sentido2 = 1

        print(f'Clic en botón {direccion}')
        print(f'Sentido: {sentido2}')

    def enviar_dato(self):
        velocidad = self.textbox_velocidad.text()
        pulsos = self.textbox_pulsos.text()

        # Verificar si los cuadros de texto no están vacíos
        if velocidad and pulsos:
            # Usa un separador reconocible, como ","
            dato = f'{velocidad},{pulsos},{sentido},{1}'
            print(f'Enviando datos: {dato}')
            self.ser.write(dato.encode())
        else:
            print("Los campos de velocidad y pulsos no pueden estar vacíos.")

    def enviar_dato2(self):
        velocidad = self.textbox_velocidad2.text()
        pulsos = self.textbox_pulsos2.text()

        # Verificar si los cuadros de texto no están vacíos
        if velocidad and pulsos:
            # Usa un separador reconocible, como ","
            dato = f'{velocidad},{pulsos},{sentido2},{2}'
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

    def validar_numeros2(self, textbox):
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
