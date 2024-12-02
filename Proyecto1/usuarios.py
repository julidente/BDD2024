import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  
            database='nombre_base_datos',  
            user='tu_usuario',  
            password='tu_contraseña'  
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def agregar_usuario(nombre, email, fecha_registro, cuota_mensual):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO Usuarios (Nombre, Email, FechaRegistro, CuotaMensual)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, email, fecha_registro, cuota_mensual))
            conexion.commit()
            print("Usuario agregado correctamente.")
        except Error as e:
            print(f"Error al agregar usuario: {e}")
        finally:
            cursor.close()
            conexion.close()

def ver_usuarios():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuarios")
            usuarios = cursor.fetchall()
            return usuarios
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

def actualizar_usuario(usuario_id, nombre=None, email=None, cuota_mensual=None):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            valores = []
            query = "UPDATE Usuarios SET "
            if nombre:
                query += "Nombre = %s, "
                valores.append(nombre)
            if email:
                query += "Email = %s, "
                valores.append(email)
            if cuota_mensual:
                query += "CuotaMensual = %s, "
                valores.append(cuota_mensual)
            query = query.rstrip(", ") + " WHERE ID = %s"
            valores.append(usuario_id)
            cursor.execute(query, valores)
            conexion.commit()
            print("Usuario actualizado correctamente.")
        except Error as e:
            print(f"Error al actualizar usuario: {e}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_usuario(usuario_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Usuarios WHERE ID = %s", (usuario_id,))
            conexion.commit()
            print("Usuario eliminado correctamente.")
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
        finally:
            cursor.close()
            conexion.close()

def buscar_usuarios_por_nombre(nombre):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM Usuarios WHERE Nombre LIKE %s"
            cursor.execute(query, (f"%{nombre}%",))
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"Error al buscar usuarios: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

def filtrar_usuarios_por_cuota(min_cuota, max_cuota):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM Usuarios WHERE CuotaMensual BETWEEN %s AND %s"
            cursor.execute(query, (min_cuota, max_cuota))
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"Error al filtrar usuarios: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

def mostrar_menu():
    print("\n=== Menú de Gestión de Usuarios ===")
    print("1. Agregar un nuevo usuario")
    print("2. Ver todos los usuarios")
    print("3. Actualizar información de un usuario")
    print("4. Eliminar un usuario")
    print("5. Buscar usuarios por nombre")
    print("6. Filtrar usuarios por cuota mensual")
    print("7. Salir")

def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            nombre = input("Ingrese el nombre: ")
            email = input("Ingrese el correo electrónico: ")
            fecha_registro = input("Ingrese la fecha de registro (YYYY-MM-DD): ")
            cuota_mensual = float(input("Ingrese la cuota mensual: "))
            agregar_usuario(nombre, email, fecha_registro, cuota_mensual)
        
        elif opcion == "2":
            usuarios = ver_usuarios()
            if usuarios:
                print("\n=== Lista de Usuarios ===")
                for usuario in usuarios:
                    print(f"ID: {usuario['ID']}, Nombre: {usuario['Nombre']}, Email: {usuario['Email']}, "
                          f"Fecha de Registro: {usuario['FechaRegistro']}, Cuota Mensual: {usuario['CuotaMensual']}")
            else:
                print("No hay usuarios registrados.")

        elif opcion == "3":
            usuario_id = int(input("Ingrese el ID del usuario a actualizar: "))
            nombre = input("Ingrese el nuevo nombre (dejar en blanco para no modificar): ") or None
            email = input("Ingrese el nuevo correo electrónico (dejar en blanco para no modificar): ") or None
            cuota_mensual = input("Ingrese la nueva cuota mensual (dejar en blanco para no modificar): ")
            cuota_mensual = float(cuota_mensual) if cuota_mensual else None
            actualizar_usuario(usuario_id, nombre, email, cuota_mensual)
        
        elif opcion == "4":
            usuario_id = int(input("Ingrese el ID del usuario a eliminar: "))
            eliminar_usuario(usuario_id)
        
        elif opcion == "5":
            nombre = input("Ingrese el nombre o parte del nombre a buscar: ")
            usuarios_filtrados = buscar_usuarios_por_nombre(nombre)
            if usuarios_filtrados:
                print("\n=== Usuarios Encontrados ===")
                for usuario in usuarios_filtrados:
                    print(f"ID: {usuario['ID']}, Nombre: {usuario['Nombre']}, Email: {usuario['Email']}, "
                          f"Fecha de Registro: {usuario['FechaRegistro']}, Cuota Mensual: {usuario['CuotaMensual']}")
            else:
                print("No se encontraron usuarios con ese nombre.")
        
        elif opcion == "6":
            min_cuota = float(input("Ingrese el mínimo de la cuota mensual: "))
            max_cuota = float(input("Ingrese el máximo de la cuota mensual: "))
            usuarios_cuota = filtrar_usuarios_por_cuota(min_cuota, max_cuota)
            if usuarios_cuota:
                print("\n=== Usuarios Encontrados por Cuota ===")
                for usuario in usuarios_cuota:
                    print(f"ID: {usuario['ID']}, Nombre: {usuario['Nombre']}, Email: {usuario['Email']}, "
                          f"Fecha de Registro: {usuario['FechaRegistro']}, Cuota Mensual: {usuario['CuotaMensual']}")
            else:
                print("No se encontraron usuarios en ese rango de cuota mensual.")
        
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
        
        else:
            print("Opción no válida. Intenta nuevamente.")

if __name__ == "__main__":
    ejecutar_menu()