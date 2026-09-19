"""
Modulo de validaciones: reglas de negocio para chequear la integridad de un Post.

Trabaja con objetos (atributos), no con diccionarios: recibe una instancia
de Post (ver modelos.py) y revisa sus atributos directamente.
"""

from .datos import estados_post


def validar_post(post):
    """
    Verifica las reglas de negocio de un post:
      1) que el titulo no este vacio,
      2) que tenga al menos un tag,
      3) que el estado no este vacio y sea uno de los estados validos,
      4) que tenga un autor con nombre.

    Retorna True si el post es valido, o un string con el detalle
    del error en caso contrario.
    """
    errores = []

    if not str(getattr(post, "titulo", "") or "").strip():
        errores.append("el titulo esta vacio")

    if not getattr(post, "tags", None):
        errores.append("no tiene tags cargados")

    estado = getattr(post, "estado", "") or ""
    if not str(estado).strip():
        errores.append("el estado esta vacio")
    elif estado not in estados_post:
        errores.append(f"el estado '{estado}' no es valido")

    autor = getattr(post, "autor", None)
    if autor is None:
        errores.append("el post no tiene autor")
    elif not getattr(autor, "nombre", None):
        errores.append("el autor no tiene nombre")

    if errores:
        return f"Post invalido (id {getattr(post, 'id', '?')}): {', '.join(errores)}."

    return True
