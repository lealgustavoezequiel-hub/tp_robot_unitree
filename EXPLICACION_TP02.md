# Resolución del TP02

Se completó mi_desarrollo/mi_tp02.py. No se modificaron robot.py, misiones.py ni el entorno.

## 1. Validación

comando_es_valido devuelve True cuando motivo_invalido devuelve una cadena vacía. La función auxiliar evita repetir las reglas y permite explicar cada rechazo.

Se comprueba, en orden: que sea una tupla, que no esté vacía, que el nombre exista y que tenga la cantidad correcta de elementos. Para avanzar y girar, velocidad y tiempo deben ser int o float; se rechazan textos, booleanos, NaN e infinito. El tiempo debe ser mayor o igual que cero. Las velocidades negativas son válidas: permiten retroceder o girar a la derecha.

Los máximos se controlan en la API del robot, como propone la consigna. Un comando puede tener formato válido y aun así ser rechazado por seguridad.

## 2. Ejecución

ejecutar_comando elige el método mediante if/elif/else y pasa velocidad y tiempo por nombre. Devuelve un texto que empieza por OK: si terminó correctamente. Captura ErrorDeSeguridad, detiene el robot y devuelve RECHAZADO: con el mensaje original. No se ocultan otros errores inesperados.

El perfil tp02 se selecciona expresamente al crear Robot. Sus límites actuales son 0,20 m/s, 0,50 rad/s y 10 segundos por movimiento. No se modificaron estos límites.

## 3. Historial

ejecutar_mision recorre todos los comandos con for. Si el formato es inválido, registra el motivo sin llamar al movimiento. Si es válido, llama a ejecutar_comando. En ambos casos agrega al historial una tupla (comando, resultado) y muestra el resultado.

Ejemplo de registro:

    (("avanzar", 0.2, 2.0), "OK: avanzar ejecutado.")

Un rechazo no termina el bucle. Un fallo de conexión inesperado sí se propaga; no se informa como si fuera un simple comando inválido.

## 4. Reporte

generar_reporte cuenta resultados que empiezan por OK: y resultados rechazados. Luego muestra cada comando rechazado junto con su motivo. También funciona con un historial vacío.

## 5. Cierre

main conserva la misión básica por defecto. El bloque finally intenta detenerse y, mediante otro finally, intenta desconectar aunque la detención falle. No completa nombre y comisión: esos datos los tiene que agregar el alumno.

## Pruebas realizadas

Se importó el controlador y se usó la clase Robot con el perfil y los validadores reales. Se sustituyeron las operaciones de movimiento, saludo y estado por objetos de prueba para no requerir una ventana del simulador.

| Misión | Correctos | Rechazados |
| --- | --- | --- |
| Básica | 4 | 0 |
| Cuadrado | 9 | 0 |
| Con errores | 4 | 7 |
| Larga | 9 | 0 |

En la misión con errores solo llegaron dos comandos a la operación de movimiento: el avance y el giro iniciales. Los tres excesos fueron rechazados por los validadores reales. Los cuatro errores de formato se rechazaron antes de ejecutar. Después se ejecutaron saludo y detención.

También se verificaron 13 casos inválidos adicionales, cuatro casos de formas o límites válidos y el reporte vacío. No se comprobó el movimiento visual en MuJoCo ni se conectó un robot físico. El cuadrado usa giros aproximados de 1,57 radianes; el retorno geométrico no es matemáticamente exacto.

## Ejecución en Windows

Desde la carpeta principal, con dependencias instaladas:

    .\INICIAR_SIMULADOR.bat

Elegir G1 y esperar que aparezca la ventana. En otra terminal, desde la misma carpeta:

    .\.venv\Scripts\python.exe mi_desarrollo\mi_tp02.py

Para probar rechazos, cambiar en main:

    ejecutar_mision(robot, MISION_BASICA, historial)

por:

    ejecutar_mision(robot, MISION_CON_ERRORES, historial)

También se puede elegir MISION_CUADRADO. No cambiar las otras funciones.

El README original menciona ejecutar_mi_codigo.bat y ejecutar_mi_codigo.sh, pero esos archivos no están incluidos: usar el comando directo anterior.

El ZIP original contiene un entorno .venv de otra computadora. Un entorno virtual no es portable: si falla, recrearlo con una instalación compatible de Python e instalar MuJoCo siguiendo el README. La solución no incorpora librerías externas nuevas; math pertenece a Python.
