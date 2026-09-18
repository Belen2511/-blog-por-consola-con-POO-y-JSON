"""
Punto de entrada del programa.

Este archivo queda AFUERA del paquete "blog": es el que ejecutas
con "python3 main.py". Se encarga de cargar (o crear) el blog desde
posts.json y de correr el bucle principal del menu.
"""

import os

from blog import (
    Blog,
    listar_posts,
    buscar_por_titulo,
    filtrar_por_tag,
    validar_posts,
    crear_post,
    obtener_opcion_menu,
)

RUTA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts.json")


def main():
    # Blog.cargar_json (via datos.cargar_posts) crea posts.json con los
    # datos iniciales si todavia no existe.
    blog = Blog.cargar_json(RUTA_JSON)

    while True:
        opcion = obtener_opcion_menu()

        if opcion == 1:
            listar_posts(blog)
        elif opcion == 2:
            buscar_por_titulo(blog)
        elif opcion == 3:
            filtrar_por_tag(blog)
        elif opcion == 4:
            validar_posts(blog)
        elif opcion == 5:
            crear_post(blog, RUTA_JSON)
        elif opcion == 6:
            print("\nSaliendo del blog. ¡Hasta la proxima!")
            break
        else:
            print("\nOpcion invalida. Por favor elegi un numero del 1 al 6.")


if __name__ == "__main__":
    main()
