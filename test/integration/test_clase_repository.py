import pytest
import psycopg2


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