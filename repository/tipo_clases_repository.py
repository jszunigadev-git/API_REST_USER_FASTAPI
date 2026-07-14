from database import conn_cursor


class TipoClasesRepository:
    
    @staticmethod
    @conn_cursor
    def obtener_tipo_clases(cursor) -> list:
        cursor.execute("SELECT * FROM tipo_clase")
        return cursor.fetchall()
    @staticmethod
    @conn_cursor
    def obtener_tipo_clase(cursor,id:int) -> dict | None:
        cursor.execute("SELECT * FROM tipo_clase WHERE id = %s",(id,))
        return cursor.fetchone()