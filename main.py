"""
Punto de entrada del programa.

Este archivo queda AFUERA del paquete "blog": es el que se ejecuta
con "python main.py". Se encarga de:
  1. Cargar los posts desde posts.json (datos.cargar_posts).
  2. Crear la instancia de Blog con esos posts.
  3. Mostrar el menu y llamar a la operacion que corresponde.
  4. Guardar los posts en posts.json (opcion 6 y al salir).
"""

import os

from blog import (
    Blog,
    cargar_posts,
    listar_posts,
    buscar_por_titulo,
    filtrar_por_tag,
    crear_post,
    validar_posts,
    guardar_posts,
    obtener_opcion_menu,
)

RUTA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts.json")


def main():
    # Carga los posts desde el JSON (ya convertidos en objetos Post)
    # y crea la instancia de Blog que usa todo el menu.
    posts = cargar_posts(RUTA_JSON)
    blog = Blog(posts)

    while True:
        opcion = obtener_opcion_menu()

        if opcion == 1:
            listar_posts(blog)
        elif opcion == 2:
            buscar_por_titulo(blog)
        elif opcion == 3:
            filtrar_por_tag(blog)
        elif opcion == 4:
            crear_post(blog)
        elif opcion == 5:
            validar_posts(blog)
        elif opcion == 6:
            guardar_posts(blog, RUTA_JSON)
        elif opcion == 7:
            # Guardado automatico antes de salir, para no perder posts nuevos.
            guardar_posts(blog, RUTA_JSON)
            print("\nSaliendo del blog. ¡Hasta la proxima!")
            break
        else:
            print("\nOpcion invalida. Por favor elegi un numero del 1 al 7.")


if __name__ == "__main__":
    main()
