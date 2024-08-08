import sqlite3
import serial
import time
from datetime import datetime

# Conectar a la base de datos
conn = sqlite3.connect('Secuencia5.db')
cursor = conn.cursor()

# Configurar el puerto serial (reemplaza '/dev/ttyUSB0' con el puerto correcto para tu Arduino)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # En Linux/Mac, podría ser '/dev/ttyUSB0' o similar
time.sleep(2)  # Espera 2 segundos para que el puerto serial se inicialice

try:
    while True:
        # Leer el valor del sensor desde el puerto serial
        if ser.in_waiting > 0:
            sensor_value = ser.readline().decode('utf-8').strip()
            
            if sensor_value.isdigit():
                sensor_value = int(sensor_value)
                # Obtener el timestamp actual
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Insertar el valor y el timestamp en la base de datos
                #print(sensor_value)
                cursor.execute('''
                    INSERT INTO mediciones (valor_sensor, timestamp) VALUES (?, ?)
                ''', (sensor_value, timestamp))
                
                # Confirmar los cambios
                conn.commit()
                print(f"Valor insertado: {sensor_value} - Timestamp: {timestamp}")
except KeyboardInterrupt:
    # Manejo de la interrupción del teclado para cerrar la conexión de manera limpia
    print("Interrupción del teclado recibida, cerrando la conexión...")
finally:
    # Cerrar la conexión con la base de datos y el puerto serial
    ser.close()
    conn.close()
