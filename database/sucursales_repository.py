from .decorators import conn_cursor


class SucursalesRepository:
    
    @conn_cursor
    def obtener_sucursales(cursor) -> list:
        cursor.execute("SELECT * FROM sucursal")
        return cursor.fetchall()
    
    @conn_cursor
    def obtener_sucursal(cursor,id:int) -> dict | None:
        cursor.execute("SELECT * FROM sucursal WHERE id = %s",(id,))
        return cursor.fetchone()