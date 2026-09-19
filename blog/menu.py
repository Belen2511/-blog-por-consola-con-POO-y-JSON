"""
Modulo de menu: interaccion con el usuario por consola.
"""


def mostrar_menu():
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Validar posts")
    print("5. Crear nuevo post")
    print("6. Salir")


def obtener_opcion_menu():
    """Muestra el menu y retorna la opcion elegida como int (o None si no es valida)."""
    mostrar_menu()
    entrada = input("Elegi una opcion (1-6): ").strip()
    try:
        return int(entrada)
    except ValueError:
        return None
