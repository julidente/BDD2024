import mysql.connector
from mysql.connector import Error
from usuarios import ver_usuarios
from libros import ver_libros

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

def validar_usuario(id_usuario):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM Usuarios WHERE ID = %s", (id_usuario,))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Error al validar el usuario: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def validar_libro(id_libro):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM Libros WHERE ID = %s", (id_libro,))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Error al validar el libro: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def registrar_prestamo(id_usuario, id_libro, fecha_prestamo, fecha_devolucion_esperada):
    if not validar_usuario(id_usuario):
        print("El ID de usuario no existe.")
        return
    if not validar_libro(id_libro):
        print("El ID de libro no existe.")
        return

    conexion = conectar()
    if conexion:
        try:
            conexion.start_transaction()
            cursor = conexion.cursor()

            # Verificar disponibilidad del libro
            cursor.execute("SELECT Disponibles FROM Libros WHERE ID = %s", (id_libro,))
            disponibles = cursor.fetchone()[0]
            if disponibles <= 0:
                print("No hay ejemplares disponibles de este libro.")
                conexion.rollback()
                return

            # Disminuir la cantidad disponible
            cursor.execute("UPDATE Libros SET Disponibles = Disponibles - 1 WHERE ID = %s", (id_libro,))

            # Registrar el préstamo
            query_prestamo = """
                INSERT INTO Prestamos (IDUsuario, IDLibro, FechaPrestamo, FechaDevolucionEsperada)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_prestamo, (id_usuario, id_libro, fecha_prestamo, fecha_devolucion_esperada))

            conexion.commit()
            print("Préstamo registrado correctamente.")
        except Error as e:
            conexion.rollback()
            print(f"Error al registrar el préstamo: {e}")
        finally:
            cursor.close()
            conexion.close()

def registrar_devolucion(id_prestamo, fecha_devolucion):
    conexion = conectar()
    if conexion:
        try:
            conexion.start_transaction()
            cursor = conexion.cursor(dictionary=True)

            # Verificar si el préstamo existe y no ha sido devuelto
            query_prestamo = "SELECT * FROM Prestamos WHERE ID = %s AND FechaDevolucion IS NULL"
            cursor.execute(query_prestamo, (id_prestamo,))
            prestamo = cursor.fetchone()

            if not prestamo:
                print("El préstamo no existe o ya ha sido devuelto.")
                conexion.rollback()
                return

            # Actualizar la fecha de devolución
            cursor.execute("UPDATE Prestamos SET FechaDevolucion = %s WHERE ID = %s", (fecha_devolucion, id_prestamo))

            # Aumentar la cantidad disponible del libro
            cursor.execute("UPDATE Libros SET Disponibles = Disponibles + 1 WHERE ID = %s", (prestamo['IDLibro'],))

            # Calcular días de retraso
            cursor.execute("SELECT DATEDIFF(%s, FechaDevolucionEsperada) AS DiasRetraso FROM Prestamos WHERE ID = %s", (fecha_devolucion, id_prestamo))
            dias_retraso = cursor.fetchone()['DiasRetraso']

            if dias_retraso > 0:
                # Obtener la cuota mensual del usuario
                cursor.execute("SELECT CuotaMensual FROM Usuarios WHERE ID = %s", (prestamo['IDUsuario'],))
                cuota_mensual = cursor.fetchone()['CuotaMensual']

                multa = dias_retraso * (cuota_mensual * 0.03)
                print(f"El usuario tiene un retraso de {dias_retraso} días. Multa: ${multa:.2f}")

                # Registrar la multa (puedes implementar cómo manejar las multas en tu sistema)
            else:
                print("Devolución realizada sin retrasos.")

            conexion.commit()
            print("Devolución registrada correctamente.")
        except Error as e:
            conexion.rollback()
            print(f"Error al registrar la devolución: {e}")
        finally:
            cursor.close()
            conexion.close()

def calcular_multa(id_usuario):
    if not validar_usuario(id_usuario):
        print("El ID de usuario no existe.")
        return

    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            query_prestamos = """
                SELECT p.ID, p.FechaDevolucionEsperada, u.CuotaMensual,
                DATEDIFF(CURDATE(), p.FechaDevolucionEsperada) AS DiasRetraso
                FROM Prestamos p
                JOIN Usuarios u ON p.IDUsuario = u.ID
                WHERE p.IDUsuario = %s AND p.FechaDevolucion IS NULL AND CURDATE() > p.FechaDevolucionEsperada
            """
            cursor.execute(query_prestamos, (id_usuario,))
            prestamos = cursor.fetchall()

            if not prestamos:
                print("No hay retrasos registrados para este usuario.")
                return

            multa_total = 0
            for prestamo in prestamos:
                dias_retraso = prestamo["DiasRetraso"]
                multa = dias_retraso * (prestamo["CuotaMensual"] * 0.03)
                multa_total += multa
                print(f"Préstamo ID {prestamo['ID']}: {dias_retraso} días de retraso, Multa: ${multa:.2f}")

            print(f"\nMulta total por retrasos: ${multa_total:.2f}")
        except Error as e:
            print(f"Error al calcular la multa: {e}")
        finally:
            cursor.close()
            conexion.close()

def modificar_cuota_mensual(id_usuario, nueva_cuota):
    if not validar_usuario(id_usuario):
        print("El ID de usuario no existe.")
        return

    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query_actualizar = """
                UPDATE Usuarios
                SET CuotaMensual = %s
                WHERE ID = %s
            """
            cursor.execute(query_actualizar, (nueva_cuota, id_usuario))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Cuota mensual actualizada correctamente.")
            else:
                print("No se pudo actualizar la cuota mensual.")
        except Error as e:
            print(f"Error al modificar la cuota mensual: {e}")
        finally:
            cursor.close()
            conexion.close()

def reporte_promedio_meses_impagos():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT u.ID, u.Nombre, u.Email,
                TIMESTAMPDIFF(MONTH,
                    IFNULL(
                        (SELECT MAX(STR_TO_DATE(CONCAT(p.Año, '-', p.Mes, '-01'), '%Y-%m-%d'))
                         FROM Pagos p WHERE p.IDUsuario = u.ID),
                        u.FechaRegistro
                    ),
                    CURDATE()
                ) AS MesesImpagos
                FROM Usuarios u
            """
            cursor.execute(query)
            usuarios_impagos = cursor.fetchall()

            # Filtrar usuarios con meses impagos mayores a 0
            usuarios_impagos = [usuario for usuario in usuarios_impagos if usuario['MesesImpagos'] > 0]

            if not usuarios_impagos:
                print("No hay usuarios con pagos pendientes.")
                return

            total_meses = sum(usuario['MesesImpagos'] for usuario in usuarios_impagos)
            promedio_meses = total_meses / len(usuarios_impagos)

            print(f"\nPromedio de meses impagos por los socios: {promedio_meses:.2f} meses.")
            print("\nDetalles de los usuarios con cuotas impagas:")
            for usuario in usuarios_impagos:
                print(f"ID: {usuario['ID']}, Nombre: {usuario['Nombre']}, Email: {usuario['Email']}, Meses Impagos: {usuario['MesesImpagos']}")
        except Error as e:
            print(f"Error al generar el reporte: {e}")
        finally:
            cursor.close()
            conexion.close()

def mostrar_menu_prestamos_y_pagos():
    print("\n=== Menú de Gestión de Préstamos y Pagos ===")
    print("1. Registrar Préstamo")
    print("2. Registrar Devolución")
    print("3. Calcular multa por retraso")
    print("4. Modificar cuota mensual de un usuario")
    print("5. Reporte de promedio de meses impagos")
    print("6. Salir")

def ejecutar_menu_prestamos_y_pagos():
    while True:
        mostrar_menu_prestamos_y_pagos()
        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            try:
                id_usuario = int(input("Ingresa el ID del usuario: "))
                id_libro = int(input("Ingresa el ID del libro: "))
                fecha_prestamo = input("Ingresa la fecha del préstamo (YYYY-MM-DD): ")
                fecha_devolucion_esperada = input("Ingresa la fecha esperada de devolución (YYYY-MM-DD): ")
                registrar_prestamo(id_usuario, id_libro, fecha_prestamo, fecha_devolucion_esperada)
            except ValueError:
                print("Por favor, ingresa valores válidos.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "2":
            try:
                id_prestamo = int(input("Ingresa el ID del préstamo: "))
                fecha_devolucion = input("Ingresa la fecha de devolución (YYYY-MM-DD): ")
                registrar_devolucion(id_prestamo, fecha_devolucion)
            except ValueError:
                print("Por favor, ingresa valores válidos.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "3":
            try:
                id_usuario = int(input("Ingresa el ID del usuario: "))
                calcular_multa(id_usuario)
            except ValueError:
                print("El ID debe ser un número entero.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "4":
            try:
                id_usuario = int(input("Ingresa el ID del usuario: "))
                nueva_cuota = float(input("Ingresa la nueva cuota mensual: "))
                modificar_cuota_mensual(id_usuario, nueva_cuota)
            except ValueError:
                print("Por favor, ingresa valores válidos.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "5":
            reporte_promedio_meses_impagos()
            input("\nPresiona Enter para continuar...")

        elif opcion == "6":
            print("Regresando al menú principal...")
            break

        else:
            print("Opción no válida. Intenta nuevamente.")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    ejecutar_menu_prestamos_y_pagos()