from database import conn_cursor
from exceptions import BaseExceptionError 


class ReservaRepository:
    
    __BASE_QUERY  = """
                SELECT
                    R.id AS id,
                    R.estado,
                    TC.nombre AS clase,
                    U.nombre AS usuario,
                    R.fecha_reserva,
                    C.fecha_hora AS fecha_hora_clase
                    FROM reserva R
                        JOIN clase C ON C.id = R.clase_id
                        JOIN tipo_clase TC ON TC.id = C.tipo_clase_id
                        JOIN usuario U ON U.id = R.usuario_id
                """
    
    @staticmethod
    @conn_cursor
    def obtener_reservas(cursor)->list:
        
        cursor.execute(ReservaRepository.__BASE_QUERY)
        return cursor.fetchall()
    
    @staticmethod
    @conn_cursor
    def obtener_reserva_by_id(cursor, reserva_id: int)->dict|None:
        cursor.execute(f"{ReservaRepository.__BASE_QUERY } WHERE R.id = %s  ",(reserva_id,))
        return cursor.fetchone()
    
    @staticmethod
    @conn_cursor
    def obtener_reservas_by_usuario(cursor, usuario_id: int)->list:
 
        cursor.execute(f"{ReservaRepository.__BASE_QUERY } WHERE R.usuario_id = %s ",(usuario_id,))
        return cursor.fetchall()      
    
    @staticmethod
    @conn_cursor
    def reserva_usuario_clase(cursor, usuario_id: int, clase_id: int)->bool :
        """Devuelve bool si existe la reserva (No cancelada) del usuario para la clase solicitada"""
        
        cursor.execute("SELECT id FROM reserva WHERE usuario_id = %s AND clase_id = %s AND estado != 'cancelada' ",(usuario_id,clase_id))
        
        if cursor.fetchone():
            return True
        return False
    
    @staticmethod
    @conn_cursor
    def crear_reserva_con_lock(cursor, usuario_id: int, clase_id: int) -> int | None:
        # 6. Verificar capacidad. # ✓ Quedan cupos (FOR UDPATE)
        # 7. Crear la reserva. # ✓ Crear reserva
        # 8. Retornar la reserva creada. # ✓ Disminuir cupos
        
        # Lock + descuento de cupo en una sola sentencia
        cursor.execute("""
            UPDATE clase 
            SET capacidad = capacidad - 1 
            WHERE id = %s AND capacidad > 0
            RETURNING id
        """, (clase_id,))
        
        clase_actualizada = cursor.fetchone()
        if not clase_actualizada:
            return None 

        cursor.execute("""
            INSERT INTO reserva (usuario_id, clase_id, estado)
            VALUES (%s, %s, 'confirmada')
            RETURNING id
        """, (usuario_id, clase_id))
        
        reserva = cursor.fetchone()
        if not reserva:
            raise BaseExceptionError("Error, No se pudo crear la reserva")

        return reserva["id"] 
    
    @staticmethod
    @conn_cursor
    def cancelar_reserva_lock(cursor,reserva_id:int)->bool:
        
        cursor.execute("""
                       UPDATE reserva 
                       SET estado = 'cancelada' 
                       WHERE estado = 'confirmada' AND id = %s 
                       RETURNING clase_id 
                       """,(reserva_id,))
        
        reserva_cancelada = cursor.fetchone()
        
        if not reserva_cancelada:
            return False
        
        clase_id = reserva_cancelada["clase_id"]
        
        cursor.execute("""
                    UPDATE clase
                    SET capacidad = capacidad + 1
                    WHERE id = %s
                    """,(clase_id,))
        
        if cursor.rowcount == 0:
            raise BaseExceptionError("Error, No se pudo cancelar la reserva")
    
        return True
        


