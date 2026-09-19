"""
Modulo de operaciones: conecta el menu (entrada del usuario) con la clase Blog.

Cada funcion de aca pide los datos que hagan falta por consola y despues
delega la logica real en el objeto Blog (ver modelos.py).
"""

from .datos import perfil_autor
from .modelos import Autor, Post


def listar_posts(blog):
    blog.listar_posts()


def buscar_por_titulo(blog):
    termino = input("Ingresa el titulo (o parte de el) a buscar: ")
    blog.buscar_por_titulo(termino)


def filtrar_por_tag(blog):
    tag = input("Ingresa el tag a filtrar: ")
    blog.filtrar_por_tag(tag)


def validar_posts(blog):
    blog.validar_todos_los_posts()


def crear_post(blog, ruta_json):
    """Pide los datos de un post nuevo, lo agrega al blog y guarda el JSON."""
    print("\n=== NUEVO POST ===")
    titulo = input("Titulo: ").strip()
    tags = [t.strip() for t in input("Tags (separados por coma): ").split(",") if t.strip()]
    estado = input("Estado (borrador/publicado/archivado): ").strip()

    autor = Autor(
        nombre=perfil_autor["nombre"],
        bio=perfil_autor["bio"],
        especialidad=perfil_autor["especialidad"],
        redes_sociales=perfil_autor["redes_sociales"],
    )
    post = Post(id=blog.siguiente_id(), titulo=titulo, autor=autor, tags=tags, estado=estado)

    blog.agregar_post(post)
    blog.guardar_json(ruta_json)
    print(f"\nPost creado y guardado en '{ruta_json}':")
    post.mostrar()
