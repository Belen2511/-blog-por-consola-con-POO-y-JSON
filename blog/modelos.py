"""
Modulo de modelos: clases que representan las entidades del blog.

Autor    -> quien escribe un post.
Post     -> una publicacion del blog (compone un Autor).
Blog     -> contenedor de posts, con la logica para listar, buscar,
            filtrar y persistir en JSON.
"""

from .datos import guardar_posts, cargar_posts
from .validaciones import validar_post


class Autor:
    """Representa a quien escribe los posts del blog."""

    def __init__(self, nombre, bio="", especialidad="", redes_sociales=None):
        self.nombre = nombre
        self.bio = bio
        self.especialidad = especialidad
        self.redes_sociales = redes_sociales if redes_sociales is not None else []

    def to_dict(self):
        """Convierte el autor a un diccionario, para poder guardarlo en JSON."""
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad": self.especialidad,
            "redes_sociales": list(self.redes_sociales),
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruye un Autor a partir de un diccionario (por ejemplo, leido de JSON)."""
        if not isinstance(data, dict):
            return None
        return cls(
            nombre=data.get("nombre", "Desconocido"),
            bio=data.get("bio", ""),
            especialidad=data.get("especialidad", ""),
            redes_sociales=data.get("redes_sociales", []),
        )

    def __str__(self):
        return self.nombre


class Post:
    """Representa una publicacion del blog. Su autor es una instancia de Autor."""

    def __init__(self, id, titulo, autor=None, tags=None, estado=""):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.tags = tags if tags is not None else []
        self.estado = estado

    def es_valido(self):
        """Aplica las reglas de negocio de validaciones.py sobre este post."""
        return validar_post(self)

    def mostrar(self):
        """Imprime el post de forma prolija, sin romper si le faltan datos."""
        nombre_autor = self.autor.nombre if isinstance(self.autor, Autor) else "Desconocido"

        print(f"  ID: {self.id if self.id is not None else '?'}")
        print(f"  Titulo: {self.titulo or '(sin titulo)'}")
        print(f"  Autor: {nombre_autor}")
        print(f"  Tags: {', '.join(self.tags) if self.tags else '(sin tags)'}")
        print(f"  Estado: {self.estado or '(sin estado)'}")
        print("  " + "-" * 30)

    def to_dict(self):
        """Convierte el post (y su autor) a un diccionario, para guardarlo en JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor.to_dict() if isinstance(self.autor, Autor) else None,
            "tags": list(self.tags),
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruye un Post (con su Autor) a partir de un diccionario."""
        return cls(
            id=data.get("id"),
            titulo=data.get("titulo", ""),
            autor=Autor.from_dict(data.get("autor")),
            tags=data.get("tags", []),
            estado=data.get("estado", ""),
        )

    def __str__(self):
        return f"Post {self.id}: {self.titulo}"


class Blog:
    """Contenedor de posts. Sabe listar, buscar, filtrar, validar y persistir en JSON."""

    def __init__(self, posts=None):
        self.posts = posts if posts is not None else []

    def agregar_post(self, post):
        """Agrega un Post al blog."""
        self.posts.append(post)
        return post

    def siguiente_id(self):
        """Calcula el proximo id disponible, en base a los posts existentes."""
        ids = [p.id for p in self.posts if isinstance(p.id, int)]
        return max(ids) + 1 if ids else 1

    def listar_posts(self):
        """Muestra todos los posts del blog."""
        print("\n=== TODOS LOS POSTS ===")
        if not self.posts:
            print("No hay posts cargados.")
            return []

        for post in self.posts:
            post.mostrar()
        return self.posts

    def buscar_por_titulo(self, termino):
        """Busca posts cuyo titulo contenga el termino dado (case-insensitive)."""
        termino = termino.strip().lower()
        encontrados = [p for p in self.posts if termino in str(p.titulo or "").lower()]

        print(f"\n=== RESULTADOS PARA '{termino}' ===")
        if not encontrados:
            print("No se encontraron posts con ese titulo.")
            return encontrados

        for post in encontrados:
            post.mostrar()
        return encontrados

    def filtrar_por_tag(self, tag):
        """Filtra posts que tengan el tag dado (case-insensitive)."""
        tag = tag.strip().lower()
        encontrados = [p for p in self.posts if tag in [t.lower() for t in p.tags]]

        print(f"\n=== POSTS CON TAG '{tag}' ===")
        if not encontrados:
            print("No se encontraron posts con ese tag.")
            return encontrados

        for post in encontrados:
            post.mostrar()
        return encontrados

    def validar_todos_los_posts(self):
        """Ejecuta validar_post() sobre cada post y muestra el resultado."""
        print("\n=== VALIDACION DE POSTS ===")
        if not self.posts:
            print("No hay posts cargados.")
            return []

        resultados = []
        for post in self.posts:
            resultado = post.es_valido()
            resultados.append((post.id, resultado))
            if resultado is True:
                print(f"  Post {post.id}: OK")
            else:
                print(f"  Post {post.id}: {resultado}")
        return resultados

    def to_dict(self):
        """Convierte todos los posts del blog a una lista de diccionarios."""
        return [post.to_dict() for post in self.posts]

    def guardar_json(self, ruta):
        """Guarda todos los posts del blog en un archivo JSON (delega en datos.py)."""
        guardar_posts(self.posts, ruta)

    @classmethod
    def cargar_json(cls, ruta):
        """Crea un Blog a partir de un archivo JSON (delega en datos.py)."""
        return cls(cargar_posts(ruta))
