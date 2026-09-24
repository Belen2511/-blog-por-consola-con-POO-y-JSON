"""
Modulo de operaciones: conecta el menu (entrada del usuario) con la clase Blog.

Cada funcion de aca pide los datos que hagan falta por consola y despues
delega la logica real en el objeto Blog (ver modelos.py).
"""

from .datos import perfil_autor, estados_post
from .menu import pedir_texto
from .modelos import Autor


def listar_posts(blog):
    blog.listar_posts()


def buscar_por_titulo(blog):
    termino = pedir_texto("Ingresa el titulo (o parte de el) a buscar: ")
    blog.buscar_por_titulo(termino)


def filtrar_por_tag(blog):
    tag = pedir_texto("Ingresa el tag a filtrar: ")
    blog.filtrar_por_tag(tag)


def validar_posts(blog):
    blog.validar_todos_los_posts()


def crear_post(blog):
    """Pide los datos de un post nuevo y lo crea con blog.crear_post()."""
    print("\n=== NUEVO POST ===")
    titulo = pedir_texto("Titulo: ")
    contenido = pedir_texto("Contenido: ")

    tags = []
    while not tags:
        tags = [t.strip() for t in input("Tags (separados por coma): ").split(",") if t.strip()]
        if not tags:
            print("  Tenes que ingresar al menos un tag.")

    estado = ""
    while estado not in estados_post:
        estado = pedir_texto(f"Estado ({'/'.join(estados_post)}): ").lower()
        if estado not in estados_post:
            print(f"  Estado invalido. Opciones: {', '.join(estados_post)}.")

    # El autor es un objeto Autor (composicion), no un diccionario suelto.
    autor = Autor.from_dict(perfil_autor)

    try:
        post = blog.crear_post(titulo, contenido, tags, estado, autor)
    except (ValueError, TypeError) as error:
        print(f"\n[ERROR] No se pudo crear el post: {error}.")
        return None

    print("\nPost creado (acordate de guardar con la opcion 6):")
    post.mostrar()
    return post


def guardar_posts(blog, ruta_json):
    """Guarda todos los posts del blog en posts.json."""
    if blog.guardar_json(ruta_json):
        print(f"\nSe guardaron {len(blog.obtener_posts())} posts en '{ruta_json}'.")
