"""
Modulo de datos: constantes del blog y persistencia en JSON.

Ademas de las constantes, este modulo es el unico que lee y escribe
posts.json usando el modulo json:
  - cargar_posts(ruta): lee el archivo y reconstruye cada Post con from_dict().
  - guardar_posts(posts, ruta): convierte cada Post a diccionario con to_dict()
    y lo guarda con json.dump().

Maneja los errores de archivo sin cerrar el programa: archivo inexistente,
vacio, con JSON invalido, con un formato inesperado o con posts incompletos.
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
        "contenido": "Instalacion de Python y primeros scripts por consola.",
        "autor": perfil_autor,
        "tags": ["python", "Principiantes"],
        "estado": "publicado",
    },
    {
        "id": 2,
        "titulo": "Analizando datos con pandas",
        "contenido": "Como cargar un CSV en un DataFrame y hacer los primeros analisis.",
        "autor": perfil_autor,
        "tags": ["python", "pandas", "DataFrames"],
        "estado": "borrador",
    },
    {
        "id": 3,
        "titulo": "Organizando datos con diccionarios",
        "contenido": "Uso de diccionarios para modelar informacion estructurada.",
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
        "contenido": "",
        "autor": None,
        "tags": [],
        "estado": "revision",
    },
]

CLAVES_REQUERIDAS = ("id", "titulo", "autor", "tags", "estado")


def guardar_posts(posts, ruta):
    """
    Convierte cada Post a diccionario (to_dict) y guarda la lista en un JSON.

    Retorna True si se guardo bien, o False si hubo un error (mostrando
    un mensaje claro en vez de cerrar el programa).
    """
    try:
        contenido = []
        for post in posts:
            # JSON no sabe guardar objetos: cada post tiene que poder
            # convertirse a diccionario antes de guardarse.
            if not hasattr(post, "to_dict"):
                raise TypeError(
                    f"no se puede guardar un {type(post).__name__} en JSON: "
                    "primero hay que convertirlo a diccionario con to_dict()"
                )
            contenido.append(post.to_dict())

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=2)
        return True

    except TypeError as error:
        print(f"[ERROR] No se pudo guardar: {error}.")
    except OSError as error:
        print(f"[ERROR] No se pudo escribir el archivo '{ruta}': {error}.")
    return False


def _posts_desde_diccionarios(lista):
    """Reconstruye objetos Post desde una lista de diccionarios, salteando los que estan mal."""
    # Import local (no al principio del archivo) para evitar un import
    # circular: modelos.py importa funciones de este modulo.
    from .modelos import Post

    posts = []
    for posicion, item in enumerate(lista, start=1):
        try:
            posts.append(Post.from_dict(item))
        except (ValueError, TypeError) as error:
            print(f"[AVISO] Se ignoro el post #{posicion} de posts.json: {error}.")
    return posts


def cargar_posts(ruta):
    """
    Carga los posts desde un archivo JSON y los devuelve como objetos Post.

    Casos que maneja sin cerrar el programa:
      - El archivo no existe: lo crea con los datos iniciales.
      - El archivo esta vacio: usa los datos iniciales.
      - El JSON es invalido o no es una lista: avisa y usa los datos iniciales
        (no pisa el archivo hasta que el usuario guarde).
      - Algun post esta incompleto: lo saltea y avisa.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        print(f"[INFO] No se encontro '{ruta}'. Se crea con los posts iniciales.")
        posts = _posts_desde_diccionarios(posts_iniciales)
        guardar_posts(posts, ruta)
        return posts
    except OSError as error:
        print(f"[ERROR] No se pudo leer '{ruta}': {error}. Se usan los posts iniciales.")
        return _posts_desde_diccionarios(posts_iniciales)

    if not texto.strip():
        print(f"[AVISO] El archivo '{ruta}' esta vacio. Se usan los posts iniciales.")
        return _posts_desde_diccionarios(posts_iniciales)

    try:
        contenido = json.loads(texto)
    except json.JSONDecodeError as error:
        print(f"[ERROR] '{ruta}' no tiene un JSON valido (linea {error.lineno}). "
              "Se usan los posts iniciales.")
        return _posts_desde_diccionarios(posts_iniciales)

    if not isinstance(contenido, list):
        print(f"[ERROR] '{ruta}' deberia contener una lista de posts. "
              "Se usan los posts iniciales.")
        return _posts_desde_diccionarios(posts_iniciales)

    return _posts_desde_diccionarios(contenido)
