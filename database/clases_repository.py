from .decorators import conn_cursor

class ClaseRepository:
    
    __BASE_QUERY = """
                       SELECT 
                       C.id AS id,
                       TC.nombre AS tipo_clase,
                       S.nombre AS sucursal,
                       E.nombre AS entrenador,
                       C.fecha_hora AS fecha_hora,
                       C.capacidad AS capacidad,
                       C.duracion_minutos AS duracion_minutos
                       FROM Clase AS C
                       JOIN tipo_clase AS TC ON TC.id = C.tipo_clase_id
                       JOIN sucursal AS S ON S.id = C.sucursal_id
                       JOIN entrenador AS E ON E.id = C.entrenador_id
                    """
    @conn_cursor
    def obtener_clases(cursor)->list:
        cursor.execute(ClaseRepository.__BASE_QUERY)
        return cursor.fetchall()
    
    @conn_cursor
    def obtener_clase(cursor,id:int)->dict | None:
        cursor.execute(f"{ClaseRepository.__BASE_QUERY} WHERE C.id = %s",(id,))
        return cursor.fetchone()
    
    @conn_cursor
    def obtener_clase_por_entrenador(cursor,id:int)->list:
        cursor.execute(f"{ClaseRepository.__BASE_QUERY} WHERE E.id = %s",(id,))
        return cursor.fetchall()
    
    
    @conn_cursor
    def obtener_clase_por_sucursal(cursor,id:int)->list:
        cursor.execute(f"{ClaseRepository.__BASE_QUERY} WHERE S.id = %s",(id,))
        return cursor.fetchall()
    
    @conn_cursor
    def obtener_clase_por_tipo_clase(cursor,id:int)->list:
        cursor.execute(f"{ClaseRepository.__BASE_QUERY} WHERE TC.id  = %s",(id,))
        return cursor.fetchall()
    
    @conn_cursor
    def crear_clase(cursor,clase:dict)->int | None:
        
        cursor.execute("""
                            INSERT INTO clase (fecha_hora, capacidad,duracion_minutos,tipo_clase_id,entrenador_id,sucursal_id)
                            VALUES
                            (   %(fecha_hora)s,
                                %(capacidad)s,
                                %(duracion_minutos)s,
                                %(tipo_clase_id)s,
                                %(entrenador_id)s,
                                %(sucursal_id)s)
                            RETURNING id
                            """,clase)
        response = cursor.fetchone()
        if  response:
            return response["id"]
        return None
    
    @conn_cursor
    def actualizar_clase(cursor,clase:dict)->bool:  
        cursor.execute("""
                       UPDATE clase SET 
                       fecha_hora = %(fecha_hora)s,
                       capacidad = %(capacidad)s,
                       duracion_minutos = %(duracion_minutos)s,
                       tipo_clase_id = %(tipo_clase_id)s,
                       entrenador_id = %(entrenador_id)s,
                       sucursal_id = %(sucursal_id)s
                       WHERE id = %(id)s
                       """,clase)
        if cursor.rowcount > 0:
            return True
        return False
    
    @conn_cursor
    def eliminar_clase(cursor,id:int)->bool:  
        cursor.execute("DELETE FROM clase WHERE id = %s",(id,))
        if cursor.rowcount > 0:
            return True
        return False
    
        