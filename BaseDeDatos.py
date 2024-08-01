import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('Secuencia5.db')

# Crear un cursor
cursor = conn.cursor()

# Crear la tabla
cursor.execute('''
    CREATE TABLE "mediciones" (
	"id_medicion"	INTEGER NOT NULL,
	"valor_sensor"	INTEGER,
	"timestamp"	TEXT,
	PRIMARY KEY("id_medicion" AUTOINCREMENT)
);
''')

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()
