

def test_conexion_a_bd_de_pruebas(db_cursor):
    db_cursor.execute("SELECT 1 AS resultado")
    fila = db_cursor.fetchone()
    assert fila["resultado"] == 1