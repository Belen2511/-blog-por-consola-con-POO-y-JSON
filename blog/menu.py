"""
Modulo de menu: interaccion con el usuario por consola.
"""


def mostrar_menu():
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Crear nuevo post")
    print("5. Validar posts")
    print("6. Guardar posts en JSON")
    print("7. Salir")


def obtener_opcion_menu():
    """Muestra el menu y retorna la opcion elegida como int (o None si no es un numero)."""
    mostrar_menu()
    entrada = input("Elegi una opcion (1-7): ").strip()
    try:
        return int(entrada)
    except ValueError:
        return None


def pedir_texto(mensaje):
    """Pide un texto por consola y lo vuelve a pedir si se deja vacio."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  Este campo no puede quedar vacio.")
