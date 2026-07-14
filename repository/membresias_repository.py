from database import conn_cursor


class MembresiaRepository:
    
    @staticmethod
    @conn_cursor
    def obtener_membresias(cursor) -> list:
        cursor.execute("SELECT * FROM membresia")
        return cursor.fetchall()
    
    @staticmethod
    @conn_cursor
    def obtener_membresia(cursor,id:int) -> dict | None:
        cursor.execute("SELECT * FROM membresia WHERE id = %s",(id,))
        return cursor.fetchone()