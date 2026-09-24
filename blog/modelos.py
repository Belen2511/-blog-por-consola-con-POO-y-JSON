"""
Modulo de modelos: clases que representan las entidades del blog.

Autor    -> quien escribe un post.
Post     -> una publicacion del blog (compone un Autor).
Blog     -> contenedor de posts: centraliza la logica para crear, listar,
            buscar, filtrar, validar y guardar posts.

Relaciones entre objetos:
    Blog  --tiene una lista de-->  Post  --tiene un-->  Autor
"""

from .datos import guardar_posts, estados_post
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
        """
        Reconstruye un Autor a partir de un diccionario leido de JSON.

        - Si data es None, devuelve None (post sin autor).
        - Si data no es un diccionario o le falta el nombre, lanza ValueError
          con un mensaje claro.
        """
        if data is None:
            return None
        if not isinstance(data, dict):
            raise ValueError(f"el autor deberia ser un diccionario y es {type(data).__name__}")
        if "nombre" not in data:
            raise ValueError("al autor le falta la clave 'nombre'")

        return cls(
            nombre=data["nombre"],
            bio=data.get("bio", ""),
            especialidad=data.get("especialidad", ""),
            redes_sociales=data.get("redes_sociales", []),
        )

    def __str__(self):
        return self.nombre


class Post:
    """Representa una publicacion del blog. Su autor es una instancia de Autor."""

    # Claves que tiene que traer un diccionario para poder reconstruir un Post.
    CLAVES_REQUERIDAS = ("id", "titulo", "autor", "tags", "estado")

    def __init__(self, id, titulo, contenido="", autor=None, tags=None, estado=""):
        if autor is not None and not isinstance(autor, Autor):
            raise TypeError("el autor de un Post tiene que ser una instancia de Autor")

        self.id = id
        self.titulo = titulo
        self.contenido = contenido
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
        print(f"  Contenido: {self.contenido or '(sin contenido)'}")
        print(f"  Tags: {', '.join(self.tags) if self.tags else '(sin tags)'}")
        print(f"  Estado: {self.estado or '(sin estado)'}")
        print("  " + "-" * 30)

    def to_dict(self):
        """Convierte el post (y su autor) a un diccionario, para guardarlo en JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.to_dict() if isinstance(self.autor, Autor) else None,
            "tags": list(self.tags),
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Reconstruye un Post (con su Autor) a partir de un diccionario.

        Lanza ValueError si data no es un diccionario, si le faltan claves
        obligatorias o si los tags no son una lista.
        """
        if not isinstance(data, dict):
            raise ValueError(f"se esperaba un diccionario y llego {type(data).__name__}")

        faltantes = [clave for clave in cls.CLAVES_REQUERIDAS if clave not in data]
        if faltantes:
            raise ValueError(f"diccionario incompleto, faltan las claves: {', '.join(faltantes)}")

        if not isinstance(data["tags"], list):
            raise ValueError("los tags tienen que ser una lista")

        return cls(
            id=data["id"],
            titulo=data["titulo"],
            contenido=data.get("contenido", ""),  # opcional: los posts viejos no lo tenian
            autor=Autor.from_dict(data["autor"]),
            tags=data["tags"],
            estado=data["estado"],
        )

    def __str__(self):
        return f"Post {self.id}: {self.titulo}"


class Blog:
    """
    Contenedor de posts. Centraliza la logica principal del sistema:
    crear, listar, buscar, filtrar, validar y guardar posts.
    """

    def __init__(self, posts=None):
        # Lista de objetos Post
        self.posts = posts if posts is not None else []

    def obtener_posts(self):
        """Devuelve todos los posts cargados en el blog."""
        return self.posts

    def agregar_post(self, post):
        """Agrega un Post ya creado al blog."""
        if not isinstance(post, Post):
            raise TypeError("solo se pueden agregar objetos Post al blog")
        self.posts.append(post)
        return post

    def siguiente_id(self):
        """Calcula el proximo id disponible, en base a los posts existentes."""
        ids = [p.id for p in self.posts if isinstance(p.id, int)]
        return max(ids) + 1 if ids else 1

    def crear_post(self, titulo, contenido, tags, estado, autor):
        """
        Crea una instancia de Post con los datos recibidos y la agrega al blog.

        Lanza ValueError si hay campos vacios o el estado no es valido.
        """
        if not titulo.strip():
            raise ValueError("el titulo no puede estar vacio")
        if not contenido.strip():
            raise ValueError("el contenido no puede estar vacio")
        if not tags:
            raise ValueError("el post tiene que tener al menos un tag")
        if estado not in estados_post:
            raise ValueError(f"el estado tiene que ser uno de: {', '.join(estados_post)}")

        post = Post(
            id=self.siguiente_id(),
            titulo=titulo.strip(),
            contenido=contenido.strip(),
            autor=autor,
            tags=tags,
            estado=estado,
        )
        return self.agregar_post(post)

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
        """Busca posts cuyo titulo contenga el termino dado (ignora mayusculas/minusculas)."""
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
        """Filtra posts que tengan el tag dado (ignora mayusculas/minusculas)."""
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
        return guardar_posts(self.posts, ruta)
