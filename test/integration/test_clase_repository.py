import pytest
import psycopg2
from datetime import datetime
from repository import ClaseRepository


def test_check_capacidad_no_puede_ser_negativa(db_cursor):
    db_cursor.execute("""
        INSERT INTO tipo_clase (id, nombre)
        VALUES (9003, 'Crossfit Test')
    """)

    with pytest.raises(psycopg2.errors.CheckViolation):
        db_cursor.execute("""
            INSERT INTO clase (id, fecha_hora, capacidad, duracion_minutos, tipo_clase_id)
            VALUES (9003, '2026-08-15 09:00:00', -1, 45, 9003)
        """)
        

def test_check_duracion_no_puede_ser_cero_o_negativa(db_cursor):
    db_cursor.execute("""
        INSERT INTO tipo_clase (id, nombre)
        VALUES (9004, 'Pilates Test')
    """)

    with pytest.raises(psycopg2.errors.CheckViolation):
        db_cursor.execute("""
            INSERT INTO clase (id, fecha_hora, capacidad, duracion_minutos, tipo_clase_id)
            VALUES (9004, '2026-08-15 09:00:00', 10, 0, 9004)
        """)
        
@pytest.mark.parametrize("metodo_obtener, key_id, es_lista",[
    (ClaseRepository.obtener_clase,"id",False),
    (ClaseRepository.obtener_clase_por_tipo_clase,"tipo_clase_id",True),
    (ClaseRepository.obtener_clase_por_sucursal,"sucursal_id",True),
    (ClaseRepository.obtener_clase_por_entrenador,"entrenador_id",True)
])   
def test_crear_y_obtener_clase(entidades_clase_base,metodo_obtener,key_id,es_lista):
    clase_dict = {
        "fecha_hora": datetime(2026, 9, 1, 10, 0),
        "capacidad": 20,
        "duracion_minutos": 45,
        **entidades_clase_base
    }

    id_clase = ClaseRepository.crear_clase(clase_dict)
    assert id_clase is not None
    
    clase_dict["id"] = id_clase
    
    id_target = clase_dict[key_id]
    resultado = metodo_obtener(id_target)
    
    if es_lista:
        assert isinstance(resultado, list)
        assert len(resultado) > 0
        ids_encontrados = [c["id"] for c in resultado]
        assert id_clase in ids_encontrados
    else:
        assert isinstance(resultado, dict)
        assert resultado["tipo_clase"] == "Tipo Test"


def test_actualizar_clase(entidades_clase_base):
    clase_dict = {
        "fecha_hora": datetime(2026, 9, 1, 10, 0),
        "capacidad": 20,
        "duracion_minutos": 45,
        **entidades_clase_base
    }
    
    id_clase = ClaseRepository.crear_clase(clase_dict)
    assert id_clase is not None
    
    clase_update_dict = {
        "id" : id_clase,
        "fecha_hora": datetime(2026, 9, 1, 10, 0),
        "capacidad": 10,
        "duracion_minutos": 60,
        **entidades_clase_base
    }
    clase_update = ClaseRepository.actualizar_clase(clase_update_dict)
    assert clase_update is True
    
    clase = ClaseRepository.obtener_clase(id_clase)
    assert clase["duracion_minutos"] == 60
    assert clase["capacidad"] == 10

 
def test_eliminar_clase(entidades_clase_base):
    clase_dict = {
        "fecha_hora": datetime(2026, 9, 1, 10, 0),
        "capacidad": 20,
        "duracion_minutos": 45,
        **entidades_clase_base
    }
    
    id_clase = ClaseRepository.crear_clase(clase_dict)
    assert id_clase is not None
    

    clase_delete = ClaseRepository.eliminar_clase(id_clase)
    assert clase_delete is True
    
