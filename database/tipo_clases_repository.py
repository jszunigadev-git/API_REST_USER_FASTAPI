from .decorators import conn_cursor


class TipoClasesRepository:
    
    @conn_cursor
    def obtener_tipo_clases(cursor) -> list:
        cursor.execute("SELECT * FROM tipo_clase")
        return cursor.fetchall()
    
    @conn_cursor
    def obtener_tipo_clase(cursor,id:int) -> dict | None:
        cursor.execute("SELECT * FROM tipo_clase WHERE id = %s",(id,))
        return cursor.fetchone()