# Este archivo hace que la carpeta "blog" sea un paquete de Python,
# es decir, que se pueda importar con "import blog" o "from blog import algo".
#
# Reexporta lo mas usado para que quede mas corto de importar desde afuera.
# Por ejemplo, en vez de escribir "from blog.modelos import Blog", alcanza
# con "from blog import Blog".

from .datos import perfil_autor, estados_post, etiquetas_blog, posts_iniciales, CLAVES_REQUERIDAS
from .modelos import Autor, Post, Blog
from .validaciones import validar_post
from .operaciones import listar_posts, buscar_por_titulo, filtrar_por_tag, validar_posts, crear_post
from .menu import mostrar_menu, obtener_opcion_menu
