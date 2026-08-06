import threading
from repository import ReservaRepository

def test_crear_reserva_con_lock_concurrencia_real(clase_con_cupo):
    usuario_id_1 = clase_con_cupo["usuario_id"]
    usuario_id_2 = clase_con_cupo["usuario_id_2"]
    clase_id = clase_con_cupo["clase_id"]

    resultados = {}

    def intentar_reserva(usuario_id, clave):
        resultado = ReservaRepository.crear_reserva_con_lock(usuario_id, clase_id)
        resultados[clave] = resultado

    hilo_1 = threading.Thread(target=intentar_reserva, args=(usuario_id_1, "hilo_1"))
    hilo_2 = threading.Thread(target=intentar_reserva, args=(usuario_id_2, "hilo_2"))

    hilo_1.start()
    hilo_2.start()

    hilo_1.join()
    hilo_2.join()

    exitos = [r for r in resultados.values() if r is not None]
    fallos = [r for r in resultados.values() if r is None]

    assert len(exitos) == 1, "Debe haber exactamente UN éxito, nunca cero ni dos"
    assert len(fallos) == 1, "Debe haber exactamente UN fallo por falta de cupo"