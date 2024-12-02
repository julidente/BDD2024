from prestamos_y_pagos import ejecutar_menu_prestamos_y_pagos
from usuarios import ejecutar_menu_usuarios
from libros import ejecutar_menu_libros

def mostrar_menu_principal():
    print("\n=== Sistema de Gestión de Biblioteca ===")
    print("1. Gestión de Usuarios")
    print("2. Gestión de Libros")
    print("3. Gestión de Préstamos y Pagos")
    print("4. Salir")

def ejecutar_menu_principal():
    while True:
        mostrar_menu_principal()
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            ejecutar_menu_usuarios()
        elif opcion == "2":
            ejecutar_menu_libros()
        elif opcion == "3":
            ejecutar_menu_prestamos_y_pagos()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intenta nuevamente.")

if __name__ == "__main__":
    ejecutar_menu_principal()
