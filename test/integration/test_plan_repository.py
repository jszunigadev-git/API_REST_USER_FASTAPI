import pytest
import psycopg2


def test_exclude_constraint_rechaza_solape_de_planes(db_cursor):
    # Setup: usuario y membresía de prueba
    db_cursor.execute("""
        INSERT INTO usuario (id, nombre, email, telefono)
        VALUES (9001, 'Usuario Test', 'test@test.com', '123456')
    """)
    db_cursor.execute("""
        INSERT INTO membresia (id, nombre, precio, duracion_meses)
        VALUES (9001, 'Membresia Test', 10000, 1)
    """)

    # Primer plan: válido, del 1 al 31 de agosto
    db_cursor.execute("""
        INSERT INTO plan (usuario_id, membresia_id, fecha_inicio, fecha_fin, estado)
        VALUES (9001, 9001, '2026-08-01', '2026-08-31', 'activo')
    """)

    # Segundo plan: se solapa con el primero (empieza el 15 de agosto, dentro del rango)
    with pytest.raises(psycopg2.errors.ExclusionViolation):
        db_cursor.execute("""
            INSERT INTO plan (usuario_id, membresia_id, fecha_inicio, fecha_fin, estado)
            VALUES (9001, 9001, '2026-08-15', '2026-09-15', 'activo')
        """)
        
