"""
Modulo de datos: constantes del blog y persistencia en JSON.

Ademas de las constantes, este modulo es el unico que sabe leer y escribir
posts.json: guardar_posts() serializa una lista de Post a disco, y
cargar_posts() la reconstruye. Si el archivo todavia no existe (primera
ejecucion del programa), cargar_posts() lo crea a partir de los datos
iniciales de aca abajo.
"""

import json

perfil_autor = {
    "nombre": "Romina Vogeli",
    "bio": "Analisis de datos y machine learning.",
    "especialidad": "Data Science",
    "redes_sociales": ["@romivogeli", "@romina_ml"],
}

estados_post = ("borrador", "publicado", "archivado")

etiquetas_blog = {"analisis_de_datos", "machine_learning", "python", "sql", "power_bi", "tableau", "excel"}

posts_iniciales = [
    {
        "id": 1,
        "titulo": "Primeros pasos con Python",
        "autor": perfil_autor,
        "tags": ["python", "Principiantes"],
        "estado": "publicado",
    },
    {
        "id": 2,
        "titulo": "Analizando datos con pandas",
        "autor": perfil_autor,
        "tags": ["python", "pandas", "DataFrames"],
        "estado": "borrador",
    },
    {
        "id": 3,
        "titulo": "Organizando datos con diccionarios",
        "autor": perfil_autor,
        "tags": ["python", "Diccionarios"],
        "estado": "archivado",
    },
    {
        # Post incompleto a proposito, para probar validar_post():
        # no tiene autor, el titulo y los tags estan vacios,
        # y "revision" no es un estado valido (no esta en estados_post).
        "id": 4,
        "titulo": "",
        "autor": None,
        "tags": [],
        "estado": "revision",
    },
]

CLAVES_REQUERIDAS = ("id", "titulo", "autor", "tags", "estado")


def guardar_posts(posts, ruta):
    """Serializa una lista de Post y la guarda en un archivo JSON."""
    contenido = [post.to_dict() for post in posts]
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(contenido, archivo, ensure_ascii=False, indent=2)


def cargar_posts(ruta):
    """
    Carga una lista de Post desde un archivo JSON.

    Si el archivo no existe (o esta corrupto), lo crea a partir de
    posts_iniciales y devuelve esos posts.
    """
    # Import local (no al principio del archivo) para evitar un import
    # circular: modelos.py necesita estas funciones de datos.py, asi que
    # datos.py no puede importar modelos.py de entrada.
    from .modelos import Post

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = [Post.from_dict(item) for item in posts_iniciales]
        guardar_posts(posts, ruta)
        return posts

    return [Post.from_dict(item) for item in contenido]
