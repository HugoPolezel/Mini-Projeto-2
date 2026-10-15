import time
import logging
from functools import wraps

logging.basicConfig(
    filename="tempo.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)


def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função e grava em log."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        duracao = fim - inicio
        logging.info(f"Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper