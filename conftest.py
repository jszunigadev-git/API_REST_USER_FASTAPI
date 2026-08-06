import pytest
from dotenv import load_dotenv
load_dotenv(".env.test", override=True)

from database.connection import get_connection
from psycopg2.extras import RealDictCursor


@pytest.fixture
def db_cursor():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    yield cursor 
    
    conn.rollback()
    cursor.close()
    conn.close()
    

@pytest.fixture
def clase_con_cupo():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO usuario (id, nombre, email, telefono)
        VALUES (9005, 'Usuario Lock Test', 'lock@test.com', '123456')
    """)
    cursor.execute("""
        INSERT INTO usuario (id, nombre, email, telefono)
        VALUES (9006, 'Usuario Lock Test 2', 'lock2@test.com', '123456')
    """)
    cursor.execute("""
        INSERT INTO tipo_clase (id, nombre)
        VALUES (9005, 'Test Lock')
    """)
    cursor.execute("""
        INSERT INTO clase (id, fecha_hora, capacidad, duracion_minutos, tipo_clase_id)
        VALUES (9005, '2026-08-20 10:00:00', 1, 45, 9005)
    """)
    conn.commit()
    cursor.close()

    yield {"usuario_id": 9005, "usuario_id_2": 9006, "clase_id": 9005}

    cursor = conn.cursor()
    cursor.execute("DELETE FROM reserva WHERE usuario_id IN (9005, 9006) OR clase_id = 9005")
    cursor.execute("DELETE FROM clase WHERE id = 9005")
    cursor.execute("DELETE FROM tipo_clase WHERE id = 9005")
    cursor.execute("DELETE FROM usuario WHERE id IN (9005, 9006)")
    conn.commit()
    cursor.close()
    conn.close()
    


@pytest.fixture
def entidades_clase_base():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO tipo_clase (id, nombre) VALUES (9010, 'Tipo Test')
    """)
    cursor.execute("""
        INSERT INTO sucursal (id, nombre) VALUES (9010, 'Sucursal Test')
    """)
    cursor.execute("""
        INSERT INTO entrenador (id, nombre, email, telefono)
        VALUES (9010, 'Entrenador Test', 'entrenador@test.com', '123456')
    """)
    conn.commit()
    cursor.close()

    yield {"tipo_clase_id": 9010, "sucursal_id": 9010, "entrenador_id": 9010}

    cursor = conn.cursor()
    cursor.execute("DELETE FROM clase WHERE tipo_clase_id = 9010 OR sucursal_id = 9010 OR entrenador_id = 9010")
    cursor.execute("DELETE FROM tipo_clase WHERE id = 9010")
    cursor.execute("DELETE FROM sucursal WHERE id = 9010")
    cursor.execute("DELETE FROM entrenador WHERE id = 9010")
    conn.commit()
    cursor.close()
    conn.close()
    

@pytest.fixture
def entidad_tipo_clase():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO tipo_clase (id, nombre) VALUES (9010, 'Tipo Clase Test')
    """)

    conn.commit()
    cursor.close()

    yield {"tipo_clase_id": 9010}

    cursor = conn.cursor()
    cursor.execute("DELETE FROM tipo_clase WHERE id = 9010")
    conn.commit()
    cursor.close()
    conn.close()
    
    

@pytest.fixture
def entidad_membresia():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO membresia (id, nombre, precio, duracion_meses) VALUES (9010, 'membresia Test', '30000', '1')
    """)

    conn.commit()
    cursor.close()

    yield {"id_membresia": 9010}

    cursor = conn.cursor()
    cursor.execute("DELETE FROM membresia WHERE id = 9010")
    conn.commit()
    cursor.close()
    conn.close()

@pytest.fixture
def entidad_sucursal():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO sucursal (id, nombre) VALUES (9010, 'Sucursal Test')
    """)

    conn.commit()
    cursor.close()

    yield {"id_sucursal": 9010}

    cursor = conn.cursor()
    cursor.execute("DELETE FROM sucursal WHERE id = 9010")
    conn.commit()
    cursor.close()
    conn.close()
    
    

@pytest.fixture
def setup_plan():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO usuario (id, nombre, email, telefono)
        VALUES (9011, 'Usuario Test', 'test@test.com', '123456')
    """)
    cursor.execute("""
        INSERT INTO membresia (id, nombre, precio, duracion_meses)
        VALUES (9012, 'Membresia Test', 10000, 1)
    """)
    
    conn.commit()
    cursor.close()

    yield {"usuario_id": 9011, "membresia_id" : 9012}

    cursor = conn.cursor()
    cursor.execute("DELETE FROM plan WHERE usuario_id = 9011 OR membresia_id = 9012")
    cursor.execute("DELETE FROM usuario WHERE id = 9011")
    cursor.execute("DELETE FROM membresia WHERE id = 9012")
    conn.commit()
    cursor.close()
    conn.close()   
