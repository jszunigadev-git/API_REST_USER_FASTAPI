import pytest
import psycopg2
from repository import ReservaRepository , ClaseRepository
from database.connection import get_connection
from psycopg2.extras import RealDictCursor

def test_indice_unico_rechaza_reserva_duplicada_activa(db_cursor):
    # Setup: usuario, membresía, tipo_clase, clase
    db_cursor.execute("""
        INSERT INTO usuario (id, nombre, email, telefono)
        VALUES (9001, 'Usuario Test', 'test@test.com', '123456')
    """)
    db_cursor.execute("""
        INSERT INTO tipo_clase (id, nombre)
        VALUES (9001, 'Spinning Test')
    """)
    db_cursor.execute("""
        INSERT INTO clase (id, fecha_hora, capacidad, duracion_minutos, tipo_clase_id)
        VALUES (9001, '2026-08-15 10:00:00', 20, 45, 9001)
    """)

    # Primera reserva: confirmada
    db_cursor.execute("""
        INSERT INTO reserva (usuario_id, clase_id, estado)
        VALUES (9001, 9001, 'confirmada')
    """)

    # Intento de reserva duplicada mientras la primera sigue activa -> debe fallar
    with pytest.raises(psycopg2.errors.UniqueViolation):
        db_cursor.execute("""
            INSERT INTO reserva (usuario_id, clase_id, estado)
            VALUES (9001, 9001, 'confirmada')
        """)


def test_indice_unico_permite_reservar_de_nuevo_tras_cancelar(db_cursor):
    db_cursor.execute("""
        INSERT INTO usuario (id, nombre, email, telefono)
        VALUES (9002, 'Usuario Test 2', 'test2@test.com', '123456')
    """)
    db_cursor.execute("""
        INSERT INTO tipo_clase (id, nombre)
        VALUES (9002, 'Yoga Test')
    """)
    db_cursor.execute("""
        INSERT INTO clase (id, fecha_hora, capacidad, duracion_minutos, tipo_clase_id)
        VALUES (9002, '2026-08-15 11:00:00', 15, 60, 9002)
    """)

    # Primera reserva: se crea y luego se cancela
    db_cursor.execute("""
        INSERT INTO reserva (usuario_id, clase_id, estado)
        VALUES (9002, 9002, 'confirmada')
    """)
    db_cursor.execute("""
        UPDATE reserva SET estado = 'cancelada' 
        WHERE usuario_id = 9002 AND clase_id = 9002
    """)

    # Nueva reserva para la misma clase -> NO debería fallar, porque la anterior está cancelada
    db_cursor.execute("""
        INSERT INTO reserva (usuario_id, clase_id, estado)
        VALUES (9002, 9002, 'confirmada')
    """)
    
    # Verificamos que ahora hay 2 filas para ese par (una cancelada, una confirmada)
    db_cursor.execute("""
        SELECT COUNT(*) AS total FROM reserva WHERE usuario_id = 9002 AND clase_id = 9002
    """)
    resultado = db_cursor.fetchone()
    assert resultado["total"] == 2
    

def test_crear_reserva_con_lock_descuenta_capacidad(clase_con_cupo):
    usuario_id = clase_con_cupo["usuario_id"]
    clase_id = clase_con_cupo["clase_id"]

    id_reserva = ReservaRepository.crear_reserva_con_lock(usuario_id, clase_id)

    assert id_reserva is not None

    # Verificamos que la capacidad efectivamente bajó a 0
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT capacidad FROM clase WHERE id = %s", (clase_id,))
    clase = cursor.fetchone()
    assert clase["capacidad"] == 0
    cursor.close()
    conn.close()
        
def test_crear_reserva_con_lock_sin_cupo_retorna_none(clase_con_cupo):
    usuario_id_1 = clase_con_cupo["usuario_id"]
    usuario_id_2 = clase_con_cupo["usuario_id_2"]
    clase_id = clase_con_cupo["clase_id"]

    # El primer usuario ocupa el único cupo disponible
    primera = ReservaRepository.crear_reserva_con_lock(usuario_id_1, clase_id)
    assert primera is not None

    # El segundo usuario (distinto) intenta reservar la misma clase, ya sin cupo
    segunda = ReservaRepository.crear_reserva_con_lock(usuario_id_2, clase_id)
    assert segunda is None
    

@pytest.mark.parametrize("obtener_funcion,key_id,es_lista",[
    (ReservaRepository.obtener_reservas,None,True),
    (ReservaRepository.obtener_reserva_by_id,"id",False),
    (ReservaRepository.obtener_reservas_by_usuario,"usuario_id",True)
])
def test_reserva_select_by(clase_con_cupo, obtener_funcion, key_id, es_lista):
    
    usuario_id = clase_con_cupo["usuario_id"]
    clase_id = clase_con_cupo["clase_id"]

    reserva_id = ReservaRepository.crear_reserva_con_lock(usuario_id, clase_id)
    
    
    assert reserva_id is not None
    
    clase_con_cupo["id"] = reserva_id
    
    if key_id:
        target_id = clase_con_cupo[key_id]
        resultado = obtener_funcion(target_id)
    else:
        resultado = obtener_funcion()
    
    if es_lista:
      assert isinstance(resultado, list)
      assert len(resultado) > 0
      id_buscado = [r["id"] for r in resultado]
      assert reserva_id in id_buscado
    
    else:
       assert isinstance(resultado, dict)
       assert resultado["id"] == reserva_id 

def test_reserva_crear_reserva_con_lock(clase_con_cupo):
    
    usuario_id = clase_con_cupo["usuario_id"]
    clase_id = clase_con_cupo["clase_id"]
    
    reserva_id = ReservaRepository.crear_reserva_con_lock(usuario_id, clase_id)
    
    assert reserva_id is not None

    resultado = ReservaRepository.reserva_usuario_clase(usuario_id, clase_id)
    
    assert isinstance(resultado, bool)
    
    assert resultado is True

  
def test_plan_cancelar_reserva_lock(clase_con_cupo):
    
    usuario_id = clase_con_cupo["usuario_id"]
    clase_id = clase_con_cupo["clase_id"]
    
    reserva_id = ReservaRepository.crear_reserva_con_lock(usuario_id, clase_id)
    
    assert reserva_id is not None

    resultado = ReservaRepository.cancelar_reserva_lock(reserva_id)
    
    assert isinstance(resultado, bool)
    
    assert resultado is True


    