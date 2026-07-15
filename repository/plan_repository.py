from database import conn_cursor
from datetime import date

class PlanRepository:
    
    __BASE_QUERY = """
                       SELECT 
                       P.id,
                       U.nombre AS nombre_usuario,
                       U.email AS email_usuario,
                       M.nombre AS membresia,
                       P.fecha_inicio,
                       P.fecha_fin,
                       P.estado
                       FROM plan AS P
                       JOIN usuario AS U ON U.id = P.usuario_id
                       JOIN membresia AS M ON M.id = P.membresia_id
    
                    """
                    
    @staticmethod
    @conn_cursor
    def obtener_planes(cursor)->list:
        cursor.execute(PlanRepository.__BASE_QUERY)
        return cursor.fetchall()
    
    @staticmethod
    @conn_cursor
    def obtener_plan_id(cursor,id:int)->dict | None:
        cursor.execute(f"{PlanRepository.__BASE_QUERY} WHERE P.id = %s",(id,))
        return cursor.fetchone()
    
    @staticmethod
    @conn_cursor
    def obtener_plan_usuario(cursor,id:int)->list:
        cursor.execute(f"{PlanRepository.__BASE_QUERY} WHERE U.id = %s",(id,))
        return cursor.fetchall()
    
    @staticmethod
    @conn_cursor
    def obtener_plan_vigente_por_usuario(cursor,id:int)->list:
        cursor.execute(f"{PlanRepository.__BASE_QUERY} WHERE P.fecha_fin >= now()::date AND U.id = %s AND P.estado = 'activo'",(id,))
        return cursor.fetchall()
    
    @staticmethod
    @conn_cursor
    def obtener_plan_vigente_entre_fecha_por_usuario(cursor,id:int,fecha_inicio:date,fecha_fin:date)->bool:
        cursor.execute(f"{PlanRepository.__BASE_QUERY} WHERE (P.fecha_inicio < %s AND P.fecha_fin > %s) AND P.estado = 'activo' AND U.id = %s",(fecha_fin,fecha_inicio,id))
        if cursor.fetchone():
            return True
        return False
    
    @staticmethod
    @conn_cursor
    def crear_plan(cursor,plan:dict)->int | None:
        
        cursor.execute("""
                            INSERT INTO plan (usuario_id,membresia_id,fecha_inicio,fecha_fin,estado)
                            VALUES
                            (   %(usuario_id)s,
                                %(membresia_id)s,
                                %(fecha_inicio)s,
                                %(fecha_fin)s,
                                %(estado)s)
                            RETURNING id
                            """,plan)
        response = cursor.fetchone()
        if  response:
            return response["id"]
        return None
    
    
    @staticmethod
    @conn_cursor
    def actualizar_plan(cursor, id:int, plan:dict)->bool:  
        
        columnas_set = ", ".join([f"{campo} = %({campo})s" for campo in plan.keys()])
        plan["id"] = id
        cursor.execute(f"""
                       UPDATE plan SET
                       {columnas_set}
                       WHERE id = %(id)s
                       """,plan)
        if cursor.rowcount > 0:
            return True
        return False
    
        