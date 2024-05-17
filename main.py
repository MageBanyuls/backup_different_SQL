from conexion import conexion
import os
import datetime


# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()

# Obtener el nombre de la base de datos
nombre_db = "miasesordb2"

# Crear un directorio para almacenar los backups si no existe
backup_dir = "backups"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Crear el nombre del archivo de respaldo
fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nombre_archivo_backup = f"{nombre_db}_backup_{fecha_actual}.sql"
ruta_archivo_backup = os.path.join(backup_dir, nombre_archivo_backup)

# Abrir el archivo de respaldo
with open(ruta_archivo_backup, 'w') as archivo:
    # Obtener la estructura de las tablas y escribirla en el archivo
    cursor.execute("SHOW TABLES")
    for tabla in cursor.fetchall():
        tabla = tabla[0]
        cursor.execute(f"SHOW CREATE TABLE {tabla}")
        create_table_query = cursor.fetchone()[1]
        archivo.write(f"{create_table_query};\n\n")

        # Obtener y escribir los datos de las tablas en el archivo
        cursor.execute(f"SELECT * FROM {tabla}")
        for fila in cursor.fetchall():
            valores = ', '.join([f"'{str(valor)}'" for valor in fila])
            archivo.write(f"INSERT INTO {tabla} VALUES ({valores});\n")
        archivo.write("\n")


# Cerrar el cursor y la conexión
cursor.close()
conexion.close()

print("Backup completado exitosamente.")