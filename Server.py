from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Función para inicializar la base de datos y crear la tabla si no existe
def init_db():
    conn = sqlite3.connect('sensores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS lecturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lectura INTEGER,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# Ruta que manejará las solicitudes POST enviadas por la ESP32
@app.route('/sensor', methods=['POST'])
def receive_data():
    data = request.json
    
    if 'lectura' in data:
        lectura = data['lectura']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Lectura del sensor: {lectura} a las {timestamp}")

        # Guardar los datos en la base de datos con el timestamp
        conn = sqlite3.connect('sensores.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO lecturas (lectura, timestamp) VALUES (?, ?)
        ''', (lectura, timestamp))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "lectura_recibida": lectura, "timestamp": timestamp}), 200
    else:
        return jsonify({"status": "error", "message": "Dato de lectura no encontrado"}), 400


# Levantar el servidor en el puerto 8000
if __name__ == '__main__':
    init_db()  # Inicializar la base de datos al iniciar el servidor
    app.run(host='0.0.0.0', port=8000)
