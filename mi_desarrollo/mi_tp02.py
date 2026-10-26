# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================



from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    return motivo_invalido(comando) == ""


def motivo_invalido(comando):
    """Devuelve el motivo del rechazo o texto vacio si es valido."""
    if not isinstance(comando, tuple):
        return "El comando debe ser una tupla."

    if len(comando) == 0:
        return "La tupla esta vacia."

    nombre = comando[0]

    if nombre not in ("avanzar", "girar", "detenerse", "saludar"):
        return "El nombre del comando no existe."

    if nombre in ("detenerse", "saludar"):
        if len(comando) != 1:
            return "Este comando no lleva parametros."

    else:
        if len(comando) != 3:
            return "Avanzar y girar requieren velocidad y tiempo."

        velocidad = comando[1]
        tiempo = comando[2]

        if type(velocidad) not in (int, float):
            return "La velocidad debe ser un numero."

        if type(tiempo) not in (int, float):
            return "El tiempo debe ser un numero."

        if tiempo < 0:
            return "El tiempo no puede ser negativo."

    return ""

# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # Tambien validamos aqui por si se llama esta funcion directamente.
    motivo = motivo_invalido(comando)
    if motivo != "":
        return "RECHAZADO: " + motivo

    try:
        nombre = comando[0]
        if nombre == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "detenerse":
            robot.detenerse()
        else:
            robot.saludar()
        return "OK: " + nombre + " ejecutado."
    except ErrorDeSeguridad as error:
        robot.detenerse()
        return "RECHAZADO: " + str(error)


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    for comando in mision:
        if comando_es_valido(comando):
            resultado = ejecutar_comando(robot, comando)
        else:
            resultado = "RECHAZADO: " + motivo_invalido(comando)
        # Cada registro guarda el comando original y su resultado.
        historial.append((comando, resultado))
        print(comando, "->", resultado)


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    ejecutados = 0
    rechazados = 0
    for comando, resultado in historial:
        if resultado.startswith("OK:"):
            ejecutados += 1
        else:
            rechazados += 1

    print("\nREPORTE FINAL")
    print("Comandos ejecutados correctamente:", ejecutados)
    print("Comandos rechazados:", rechazados)
    if rechazados > 0:
        print("Motivos de rechazo:")
        for comando, resultado in historial:
            if resultado.startswith("RECHAZADO:"):
                print("-", comando, "->", resultado)
    else:
        print("No hubo rechazos.")


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot(materia="tp02")
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        try:
            robot.detenerse()
        finally:
            robot.desconectar()


if __name__ == "__main__":
    main()
