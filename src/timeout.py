import signal
import time


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException()


def ejecutar_con_timeout(func, args, timeout_seconds=30):
    """
    Ejecuta una función con un timeout máximo.

    Args:
        func: Función a ejecutar
        args: Tupla de argumentos para la función
        timeout_seconds: Tiempo máximo en segundos

    Returns:
        (resultado, tiempo, timeout_ocurrido)
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)

    start_time = time.time()
    timeout_ocurrido = False
    resultado = None

    try:
        resultado = func(*args)
        signal.alarm(0)  # Cancelar alarma
    except TimeoutException:
        signal.alarm(0)
        timeout_ocurrido = True
    except Exception as e:
        signal.alarm(0)
        print(f"    ERROR: {type(e).__name__}: {e}")
        timeout_ocurrido = False
        resultado = None

    tiempo_ejecucion = time.time() - start_time

    return resultado, tiempo_ejecucion, timeout_ocurrido
