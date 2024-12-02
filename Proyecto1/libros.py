import mysql.connector
from mysql.connector import Error

# Configuración de la conexión a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  # Cambia por tu configuración
            database='nombre_base_datos',  # Cambia por el nombre de tu BD
            user='tu_usuario',  # Cambia por tu usuario
            password='tu_contraseña'  # Cambia por tu contraseña
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# 1. Registrar nuevos libros
def registrar_libro(titulo, autor, año_publicacion, disponibles):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO Libros (Titulo, Autor, AñoPublicacion, Disponibles)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (titulo, autor, año_publicacion, disponibles))
            conexion.commit()
            print("Libro registrado correctamente.")
        except Error as e:
            print(f"Error al registrar el libro: {e}")
        finally:
            cursor.close()
            conexion.close()

# 2. Ver detalles de todos los libros
def ver_libros():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Libros")
            libros = cursor.fetchall()
            return libros
        except Error as e:
            print(f"Error al obtener los libros: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

# 3. Actualizar información de un libro
def actualizar_libro(libro_id, titulo=None, autor=None, año_publicacion=None, disponibles=None):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            valores = []
            query = "UPDATE Libros SET "
            if titulo:
                query += "Titulo = %s, "
                valores.append(titulo)
            if autor:
                query += "Autor = %s, "
                valores.append(autor)
            if año_publicacion:
                query += "AñoPublicacion = %s, "
                valores.append(año_publicacion)
            if disponibles is not None:
                query += "Disponibles = %s, "
                valores.append(disponibles)
            query = query.rstrip(", ") + " WHERE ID = %s"
            valores.append(libro_id)
            cursor.execute(query, valores)
            conexion.commit()
            print("Información del libro actualizada correctamente.")
        except Error as e:
            print(f"Error al actualizar el libro: {e}")
        finally:
            cursor.close()
            conexion.close()

# 4. Eliminar un libro
def eliminar_libro(libro_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Libros WHERE ID = %s", (libro_id,))
            conexion.commit()
            print("Libro eliminado correctamente.")
        except Error as e:
            print(f"Error al eliminar el libro: {e}")
        finally:
            cursor.close()
            conexion.close()

# 5. Búsqueda y filtrado
def buscar_libros_por_titulo(titulo):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM Libros WHERE Titulo LIKE %s"
            cursor.execute(query, (f"%{titulo}%",))
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"Error al buscar libros: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

def filtrar_libros_por_año(min_año, max_año):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM Libros WHERE AñoPublicacion BETWEEN %s AND %s"
            cursor.execute(query, (min_año, max_año))
            resultados = cursor.fetchall()
            return resultados
        except Error as e:
            print(f"Error al filtrar libros: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

def mostrar_menu_libros():
    print("\n=== Menú de Gestión de Libros ===")
    print("1. Registrar un nuevo libro")
    print("2. Ver todos los libros")
    print("3. Actualizar información de un libro")
    print("4. Eliminar un libro")
    print("5. Buscar libros por título")
    print("6. Filtrar libros por año de publicación")
    print("7. Salir")

def ejecutar_menu_libros():
    while True:
        mostrar_menu_libros()
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor: ")
            año_publicacion = int(input("Ingrese el año de publicación: "))
            disponibles = int(input("Ingrese la cantidad disponible: "))
            registrar_libro(titulo, autor, año_publicacion, disponibles)
        
        elif opcion == "2":
            libros = ver_libros()
            if libros:
                print("\n=== Lista de Libros ===")
                for libro in libros:
                    print(f"ID: {libro['ID']}, Título: {libro['Titulo']}, Autor: {libro['Autor']}, "
                          f"Año de Publicación: {libro['AñoPublicacion']}, Disponibles: {libro['Disponibles']}")
            else:
                print("No hay libros registrados.")
        
        elif opcion == "3":
            libro_id = int(input("Ingrese el ID del libro a actualizar: "))
            titulo = input("Ingrese el nuevo título (dejar en blanco para no modificar): ") or None
            autor = input("Ingrese el nuevo autor (dejar en blanco para no modificar): ") or None
            año_publicacion = input("Ingrese el nuevo año de publicación (dejar en blanco para no modificar): ")
            año_publicacion = int(año_publicacion) if año_publicacion else None
            disponibles = input("Ingrese la nueva cantidad disponible (dejar en blanco para no modificar): ")
            disponibles = int(disponibles) if disponibles else None
            actualizar_libro(libro_id, titulo, autor, año_publicacion, disponibles)
        
        elif opcion == "4":
            libro_id = int(input("Ingrese el ID del libro a eliminar: "))
            eliminar_libro(libro_id)
        
        elif opcion == "5":
            titulo = input("Ingrese el título o parte del título a buscar: ")
            libros_filtrados = buscar_libros_por_titulo(titulo)
            if libros_filtrados:
                print("\n=== Libros Encontrados ===")
                for libro in libros_filtrados:
                    print(f"ID: {libro['ID']}, Título: {libro['Titulo']}, Autor: {libro['Autor']}, "
                          f"Año de Publicación: {libro['AñoPublicacion']}, Disponibles: {libro['Disponibles']}")
            else:
                print("No se encontraron libros con ese título.")
        
        elif opcion == "6":
            min_año = int(input("Ingrese el año mínimo de publicación: "))
            max_año = int(input("Ingrese el año máximo de publicación: "))
            libros_filtrados = filtrar_libros_por_año(min_año, max_año)
            if libros_filtrados:
                print("\n=== Libros Encontrados ===")
                for libro in libros_filtrados:
                    print(f"ID: {libro['ID']}, Título: {libro['Titulo']}, Autor: {libro['Autor']}, "
                          f"Año de Publicación: {libro['AñoPublicacion']}, Disponibles: {libro['Disponibles']}")
            else:
                print("No se encontraron libros en ese rango de años.")
        
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
        
        else:
            print("Opción no válida. Intenta nuevamente.")

if __name__ == "__main__":
    ejecutar_menu_libros()
