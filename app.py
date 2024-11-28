from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pymysql

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Configuración de la conexión a la base de datos RDS en AWS
db_config = {
    "host": "instancia-db-iot.cl2a0ms6etrs.us-east-1.rds.amazonaws.com",
    "user": "admin",          # Reemplaza con tu usuario de RDS
    "password": "Admin12345#!",    # Reemplaza con tu contraseña de RDS
    "database": "db_iot"  # Reemplaza con el nombre de tu base de datos
}

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

class bdAPI:
    def __init__(self):
        pass

    # Método para obtener el último registro
    def get_last(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM IoTCarStatus ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            data = {"id": row[0], "status": row[1], "ip_client": row[2], "name": row[3], "date": row[4], "id_device": row[5]}
            cursor.close()
            conn.close()
            return jsonify({"message": "Último registro recuperado correctamente", "data": data, "status": "success"}), 200
        except Exception as e:
            return jsonify({"message": str(e), "status": "error"}), 500

    # Método para obtener los últimos 10 registros
    def get_last_ten(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM IoTCarStatus ORDER BY id DESC LIMIT 10")
            rows = cursor.fetchall()
            data = [{"id": row[0], "status": row[1], "ip_client": row[2], "name": row[3], "date": row[4], "id_device": row[5]} for row in rows]
            cursor.close()
            conn.close()
            return jsonify({"message": "Últimos 10 registros recuperados correctamente", "data": data, "status": "success"}), 200
        except Exception as e:
            return jsonify({"message": str(e), "status": "error"}), 500

# Clase ItemAPI con métodos CRUD en OOP
class ItemAPI:
    def __init__(self):
        pass

     # Método GET
    def get(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM IoTCarStatus ORDER BY id DESC LIMIT 10")  
            rows = cursor.fetchall()
            data = [{"id": row[0], "status": row[1], "ip_client": row[2], "name": row[3], "date": row[4], "id_device": row[5]} for row in rows]  # Modifica las columnas según tu tabla
            cursor.close()
            conn.close()
            return jsonify({"message": "Datos recuperados correctamente", "data": data, "status": "success"}), 200
        except Exception as e:
            return jsonify({"message": str(e), "status": "error"}), 500
        
        # Método POST
    def post(self):
        # Obtener los datos JSON enviados desde el cliente
        data = request.get_json()
        button_id = data.get("id")
        status = data.get("status")
        ip_client =  request.headers.get('X-Forwarded-For', request.remote_addr)
        name = data.get("name")
        date = data.get("date")
        id_device = data.get("ip_device")

        try:
            # Conectar a la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Sentencia SQL para insertar los datos en la tabla
            cursor.execute(
                """
                INSERT INTO IoTCarStatus ( status, ip_client, name, id_device) 
                VALUES ( %s, %s, %s, %s)
                """,
                ( status, ip_client, name, id_device)
            )
            
            # Confirmar la transacción
            conn.commit()
            
            # Cerrar conexión y cursor
            cursor.close()
            conn.close()
            
            # Respuesta exitosa
            return jsonify({"message": "POST: Datos insertados correctamente", "status": "success"}), 201
        except Exception as e:
            # Respuesta de error en caso de excepción
            return jsonify({"message": str(e), "status": "error"}), 500
        

        # Método PUT
    def put(self):
        data = request.get_json()
        button_id = 1 # Recibe el ID del botón
        new_status = data.get("status")  # Recibe el nuevo valor

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Actualiza el campo en la base de datos según el ID del botón
            cursor.execute("UPDATE IoTCarStatus SET status = %s WHERE id = %s", (new_status, button_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "PUT: Datos actualizados correctamente", "status": "success"}), 200
        except Exception as e:
            return jsonify({"message": str(e), "status": "error"}), 500



# Instanciación de la clase ItemAPI
item_api = ItemAPI()
bd_api = bdAPI()

# Ruta para la página web (HTML)
@app.route('/')
def mostrar_index():
    return render_template('index.html')

# Ruta para la página web (HTML)
@app.route('/monitor')
def mostrar_monitor():
    return render_template('monitor.html')

# Ruta para api que manda un json con el último registro de la base de datos
@app.route('/api/bd', methods=['GET'])
def obtener_ultimo_item_bd():
    return bd_api.get_last()

# Ruta para api que manda un json con los últimos 10 registros de la base de datos
@app.route('/api/bd10', methods=['GET'])
def obtener_ultimos_diez_items_bd():
    return bd_api.get_last_ten()

# Rutas para la API (CRUD)
@app.route('/api/item', methods=['GET'])
def obtener_item_api():
    return item_api.get()

@app.route('/api/item', methods=['POST'])
def crear_item_api():
    return item_api.post()

@app.route('/api/item', methods=['PUT'])
def actualizar_item_api():
    return item_api.put()

@app.route('/api/item', methods=['DELETE'])
def eliminar_item_api():
    return item_api.delete()

if __name__ == '__main__':
    app.run(debug=True)
