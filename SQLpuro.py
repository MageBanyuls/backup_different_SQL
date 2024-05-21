from conexion import conexion
import os
import datetime

# Definir el orden de las tablas
orden_tablas = [
    "usuarios", "subusuarios", "listas_de_precio", "condicion_pago", "proveedores", "bancos","cuentas_banco",
    "pagos", "documento_venta","monedas", "documento_compra", "empresa", "transportista", "documento_despacho",
    "productos", "cuenta_tipo_documento", "clientes", "cobros", "categoria_cuenta",
    "administracion_por_cobrar",  "servicios",
    "e_commerce", "orden_compra", "item_servicios", "factura_venta", "factura_venta_excenta",
    "item_servicio_factura_venta", "item_servicio_factura_venta_excenta",
    "factura_compra","factura_compra_excenta", "item_servicio_factura_compra", "receta_servicios", "item_receta_servicios",
    "item_producto_documento_venta", "item_servicio_documento_despacho", "notas_de_credito_debito",
    "voucher_venta", "contactos_por_cliente", "vendedores_por_contacto", "administracion_anticipo",
    "administracion_impuesto", "administracion_por_cobrar", "proyectos", "agendamiento_proyecto",
    "anticipos_cliente", "anticipos_proveedor", "item_servicio_voucher_venta", "proveedor_productos",
    "consultas", "permisos", "permisos_de_usuario", "productos_lista_de_precios", "modulos_configuracion",
    "para_clientes_proyectos", "facturacion_electronica", "empresa_proyecto", "sistema",
    "administracion_por_pagar", "para_clientes_orden_compra", "cobranzas", "para_clientes_documentos_venta",
    "documento_despacho_traslado", "item_producto_documento_despacho_traslado",
    "item_producto_factura_compra", "notas_de_credito_debito_compras", "item_producto_nota_credito_compra",
    "documento_despacho_venta", "item_producto_documento_despacho_venta", "orden_trabajo",
    "item_despacho_venta_ot", "item_producto_factura_venta_excenta", "item_producto_factura_voucher_venta",
    "condiciones_condicion_pago","puntos_de_despacho_por_cliente", "costos_por_proyecto",
    "direccion_de_prestacion_proyecto", "item_despacho_traslado_ot", "item_producto",
    "item_receta_productos", "receta_productos",
    "item_servicio_nota_credito_compra", "nota_factura_venta", "nota_factura_venta_excenta",
    "puntos_de_despacho_por_cliente", "item_servicio_documento_venta", "item_producto_proyecto",
    "item_servicio_proyecto", "link_fintoc_bancos", "cuentasBancarias", "movimientos_cuenta", "cobros_factura_venta",
    "cobros_factura_venta_excenta","cobros_factura_nota_credito","pagos_factura_compra","pagos_factura_nota_credito",
    "cuenta_banco_conciliacion","item_producto_nota_credito_NC","item_servicio_nota_credito","item_servicio_nota_credito_NC",
    "nota_credito_nota_NC","item_producto_factura_compra_excenta","item_servicio_factura_compra_excenta", "item_producto_nota_credito_NC_compra",
    "item_servicio_nota_credito_NC_compra","nota_credito_nota_NC_compra","nota_factura_compra_excenta",
    "nota_factura_compra", "administracion_por_clasificar", "item_producto_factura_venta", "item_producto_nota_credito",
    "pagos_factura_compra_excenta","item_servicio_factura_venta", "orden_trabajo_FVE", "orden_trabajo_FV"


]



# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()

# Obtener el nombre de la base de datos
nombre_db = "miasesordb2"

# Crear un directorio para almacenar los backups si no existe
backup_dir = "backups-SQLPURO"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Crear el nombre del archivo de respaldo
fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nombre_archivo_backup = f"{nombre_db}_backup_{fecha_actual}.sql"
ruta_archivo_backup = os.path.join(backup_dir, nombre_archivo_backup)

# Abrir el archivo de respaldo
with open(ruta_archivo_backup, 'w') as archivo:
    # Iterar sobre las tablas en el orden deseado
    for tabla in orden_tablas:
        # Obtener la estructura de la tabla y escribirla en el archivo
        cursor.execute(f"SHOW CREATE TABLE {tabla}")
        create_table_query = cursor.fetchone()[1]

        # Transformar las definiciones de claves foráneas
        lines = create_table_query.split("\n")
        for i, line in enumerate(lines):
            if "KEY" in line:
                # Excluir las claves primarias
                if "PRIMARY" in line:
                    continue
                # Extraer el nombre de la columna
                referenced_table = line.split('`')[1]
                # Obtener el nombre de la tabla referenciada
                column_name = line.split('`')[3]
                # Generar la sentencia FOREIGN KEY
                new_line = f"FOREIGN KEY ({column_name}) REFERENCES {referenced_table}(id)"
                # Agregar coma si no es la penúltima línea
                if i < len(lines) - 2:
                    new_line += ","
                create_table_query = create_table_query.replace(line, new_line)

        archivo.write(f"{create_table_query};\n\n")

        # Obtener y escribir los datos de la tabla en el archivo
        cursor.execute(f"SELECT * FROM {tabla}")
        for fila in cursor.fetchall():
            # Convertir valores None a NULL
            valores = ', '.join([f"'{str(valor)}'" if valor is not None else "NULL" for valor in fila])
            archivo.write(f"INSERT INTO {tabla} VALUES ({valores});\n")
        archivo.write("\n")

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()

print("Backup completado exitosamente.")
