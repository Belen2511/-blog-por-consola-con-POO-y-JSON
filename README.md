# Blog por consola - Version POO + JSON (Preentrega 6)

Sistema de blog que se maneja desde la consola. Permite **listar, buscar,
filtrar, crear y validar posts**, y **guardarlos en un archivo `posts.json`**
para que se conserven entre una ejecucion y otra.

En esta version el sistema esta modelado con **Programacion Orientada a
Objetos**: las entidades del blog son clases (`Autor`, `Post`, `Blog`) y los
datos se guardan y se cargan usando el modulo `json`.

## Como ejecutarlo

Requisito: Python 3.8 o superior. No usa librerias externas.

Desde la carpeta raiz del proyecto (la que contiene `main.py`):

```bash
python main.py
```

Si `posts.json` no existe, el programa lo crea solo con los posts iniciales.

## Estructura del proyecto

```
blog_consola/
│
├── main.py              # Punto de entrada: carga posts.json, crea el Blog y corre el menu
├── README.md
├── posts.json           # Persistencia: aca se guardan los posts
│
└── blog/                # Paquete del sistema
    ├── __init__.py      # Marca la carpeta como paquete y reexporta lo mas usado
    ├── datos.py         # Constantes + cargar_posts() / guardar_posts() con json
    ├── menu.py          # Menu, lectura de la opcion y pedir_texto()
    ├── modelos.py       # Clases Autor, Post y Blog
    ├── operaciones.py   # Conecta cada opcion del menu con los metodos del Blog
    └── validaciones.py  # validar_post(): reglas de negocio sobre un Post
```

## Clases principales (`blog/modelos.py`)

```
Blog  --tiene una lista de-->  Post  --tiene un-->  Autor
```

| Clase | Atributos | Responsabilidad |
|---|---|---|
| `Autor` | `nombre`, `bio`, `especialidad`, `redes_sociales` | Representa a quien escribe los posts. Reemplaza al diccionario `perfil_autor` en el funcionamiento del sistema. |
| `Post` | `id`, `titulo`, `contenido`, `autor`, `tags`, `estado` | Representa una publicacion. Su atributo `autor` **es una instancia de `Autor`** (composicion); si se le pasa otra cosa lanza `TypeError`. Sabe mostrarse (`mostrar()`) y validarse (`es_valido()`). |
| `Blog` | `posts` (lista de objetos `Post`) | Centraliza la logica del sistema: `obtener_posts()`, `crear_post()`, `agregar_post()`, `listar_posts()`, `buscar_por_titulo()`, `filtrar_por_tag()`, `validar_todos_los_posts()`, `to_dict()` y `guardar_json()`. |

### Conversion entre objetos y diccionarios

JSON no puede guardar objetos de Python, asi que cada clase sabe convertirse:

- `Autor.to_dict()` / `Post.to_dict()`: objeto -> diccionario (para guardar).
- `Autor.from_dict(d)` / `Post.from_dict(d)`: diccionario -> objeto (al cargar).
- `Blog.to_dict()`: lista de posts -> lista de diccionarios.

`from_dict()` controla que el diccionario este completo (claves `id`,
`titulo`, `autor`, `tags`, `estado`) y lanza `ValueError` con un mensaje claro
si falta algo o si algun dato tiene un tipo incorrecto.

## Persistencia con JSON (`blog/datos.py`)

**Carga** – `cargar_posts(ruta)`:

1. Al iniciar, `main.py` llama a `cargar_posts("posts.json")`.
2. Se lee el archivo con `json.loads()` y cada diccionario se convierte en un
   objeto `Post` con `Post.from_dict()` (que a su vez crea el `Autor`).
3. Con esa lista de objetos, `main.py` crea la instancia: `blog = Blog(posts)`.

**Guardado** – `guardar_posts(posts, ruta)`:

1. Se llama desde `Blog.guardar_json()` (opcion 6 del menu y al salir).
2. Cada `Post` se convierte a diccionario con `to_dict()`.
3. Se escribe la lista en `posts.json` con `json.dump()`.

### Manejo de errores

| Situacion | Que hace el programa |
|---|---|
| `posts.json` no existe | Avisa y lo crea con los posts iniciales. |
| `posts.json` esta vacio | Avisa y usa los posts iniciales. |
| `posts.json` tiene JSON invalido | Muestra el error (con la linea) y usa los posts iniciales, sin cerrarse. |
| `posts.json` no contiene una lista | Avisa y usa los posts iniciales. |
| Un post del JSON esta incompleto | Lo saltea y avisa que claves le faltan. |
| Se intenta guardar algo que no es un objeto con `to_dict()` | Muestra un error claro y no rompe el archivo. |
| Opcion de menu incorrecta | Avisa y vuelve a mostrar el menu. |
| Campos vacios al crear un post | Vuelve a pedir el dato hasta que se complete. |
| Estado invalido al crear un post | Muestra los estados validos y lo vuelve a pedir. |

## Opciones del menu

```
--- MENU DEL BLOG ---
1. Ver todos los posts
2. Buscar por titulo
3. Filtrar por tag
4. Crear nuevo post
5. Validar posts
6. Guardar posts en JSON
7. Salir
```

1. **Ver todos los posts**: `blog.listar_posts()`; muestra id, titulo, autor, contenido, tags y estado.
2. **Buscar por titulo**: `blog.buscar_por_titulo()`; ignora mayusculas y minusculas.
3. **Filtrar por tag**: `blog.filtrar_por_tag()`; ignora mayusculas y minusculas.
4. **Crear nuevo post**: pide titulo, contenido, tags y estado; `blog.crear_post()` crea la instancia de `Post` (con un `Autor`) y la agrega a la lista del blog.
5. **Validar posts**: `blog.validar_todos_los_posts()` aplica `validar_post()` a cada objeto. El post con id 4 esta incompleto a proposito para probar las validaciones.
6. **Guardar posts en JSON**: `blog.guardar_json()` guarda todo en `posts.json`.
7. **Salir**: guarda automaticamente y muestra un mensaje de despedida.

## Que cambio respecto al checkpoint anterior (Modulo 5)

| Antes (Modulo 5) | Ahora (Modulo 6) |
|---|---|
| Los posts eran diccionarios en una lista dentro de `datos.py`. | Los posts son objetos `Post`, guardados en la lista `Blog.posts`. |
| El autor era un diccionario anidado. | El autor es un objeto `Autor` (composicion). |
| Las funciones de `operaciones.py` recibian la lista y hacian toda la logica. | La logica esta en metodos de `Blog`; `operaciones.py` solo pide datos y llama a esos metodos. |
| Los datos vivian solo en memoria: se perdian al cerrar. | Se cargan desde `posts.json` al iniciar y se guardan en el mismo archivo. |
| No se podian crear posts. | Opcion 4 para crear posts y opcion 6 para guardarlos. |
| `validar_post()` revisaba claves de un diccionario. | `validar_post()` revisa atributos de un objeto `Post`. |
| Nuevo archivo: — | `blog/modelos.py` y `posts.json`. |

## Como probarlo

1. Borrar `posts.json` y ejecutar `python main.py`: se crea de nuevo.
2. Crear un post (opcion 4) y guardarlo (opcion 6).
3. Salir (opcion 7) y volver a ejecutar: el post nuevo sigue estando.
4. Buscar por titulo y filtrar por tag usando mayusculas/minusculas mezcladas.
5. Ingresar una opcion invalida (por ejemplo `9` o `abc`).
