# Sistema de Blog por Consola - Version POO + JSON

Blog manejado desde la consola, ahora modelado con clases (`Autor`, `Post`,
`Blog`) y con persistencia en un archivo `posts.json`: los posts que se
crean durante la ejecucion quedan guardados y se recuperan la proxima vez
que se corre el programa.

Este proyecto es la evolucion del blog por funciones y modulos de las
preentregas anteriores: la misma logica de listar, buscar, filtrar y
validar posts, pero reorganizada en objetos en lugar de diccionarios
sueltos.

## Como ejecutarlo

```bash
python3 main.py
```

(Tiene que ejecutarse desde esta carpeta, la que contiene `main.py`, para
que los imports del paquete `blog` funcionen y `posts.json` se cree/lea al
lado de `main.py`.)

## Estructura

```
main.py                <- punto de entrada, corre el bucle principal del menu
posts.json              <- persistencia: los posts se leen y guardan aca
blog/                    <- el paquete
├── __init__.py          <- marca la carpeta como paquete y reexporta lo mas usado
├── datos.py             <- constantes + guardar_posts()/cargar_posts() (persistencia JSON)
├── modelos.py           <- clases Autor, Post y Blog
├── validaciones.py      <- validar_post(): reglas de negocio sobre un Post
├── operaciones.py       <- conecta el menu con el Blog (pide datos, llama a sus metodos)
└── menu.py              <- mostrar_menu()/obtener_opcion_menu(): solo entrada/salida
```

## Las clases (`blog/modelos.py`)

- **`Autor`**: nombre, bio, especialidad y redes sociales de quien escribe.
  Sabe convertirse a diccionario (`to_dict`) y reconstruirse desde uno
  (`from_dict`), para poder guardarse en JSON.
- **`Post`**: id, titulo, tags, estado y un **`autor`**, que es una
  instancia de `Autor` (composicion: un post "tiene un" autor, no un
  diccionario suelto). Tiene `mostrar()` para imprimirse por consola,
  `es_valido()` para chequear sus propias reglas de negocio, y
  `to_dict()`/`from_dict()` para serializarse.
- **`Blog`**: guarda una lista de `Post` y concentra la logica del
  sistema: `agregar_post`, `listar_posts`, `buscar_por_titulo`,
  `filtrar_por_tag`, `validar_todos_los_posts`, y `guardar_json()` /
  `cargar_json()` (classmethod) para la persistencia.

## Persistencia con JSON

- **`blog/datos.py`** es el unico modulo que lee y escribe archivos: tiene
  `guardar_posts(posts, ruta)` (serializa cada `Post` con `to_dict()` y
  hace `json.dump`) y `cargar_posts(ruta)` (hace `json.load` y reconstruye
  cada `Post` con `Post.from_dict()`).
- Si `posts.json` todavia no existe (primera ejecucion), `cargar_posts()`
  lo crea a partir de los datos iniciales (`posts_iniciales`) que estan en
  el mismo archivo.
- La clase `Blog` no sabe de archivos: sus metodos `guardar_json()` y
  `cargar_json()` delegan directamente en las funciones de `datos.py`. Asi,
  la logica de objetos (`modelos.py`) queda separada de la logica de
  persistencia (`datos.py`).
- Cada vez que se crea un post nuevo desde el menu (opcion 5), se guarda
  al toque en `posts.json`, para no perder el post si se cierra el
  programa.

## Por que esta separacion

- **`datos.py`** no depende de las clases al importarse (evita un import
  circular con `modelos.py`: recien importa `Post` adentro de
  `cargar_posts()`, cuando la funcion se ejecuta).
- **`modelos.py`** define el "que es cada cosa" (Autor, Post, Blog) y su
  comportamiento propio, pero no hace `input()`/`print()` de menu ni pide
  datos al usuario.
- **`validaciones.py`** separa las reglas de negocio de la clase `Post`:
  `validar_post()` recibe un post y revisa sus atributos (titulo, tags,
  estado, autor), sin mezclarse con la logica de guardado ni de consola.
- **`operaciones.py`** es el puente entre el menu y el `Blog`: pide los
  datos que hagan falta por `input()` y despues delega en los metodos del
  `Blog` (por ejemplo, `crear_post()` arma un `Post` con un `Autor` y
  llama a `blog.agregar_post()` + `blog.guardar_json()`).
- **`menu.py`** no sabe nada del resto: solo muestra las opciones y
  devuelve el numero elegido.
- **`main.py`** es el unico lugar que conoce y conecta todas las piezas:
  carga el `Blog` desde `posts.json` al arrancar, y corre el bucle
  `while True` del menu.
