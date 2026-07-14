from database import conn_cursor

class trainerRepository:
    
    @staticmethod
    @conn_cursor
    def obtener_entrenadores(cursor) -> list:
        
        cursor.execute("SELECT * FROM entrenador")
        return cursor.fetchall()
    
    @staticmethod
    @conn_cursor
    def obtener_entrenador(cursor,id: int) -> dict:
        
        cursor.execute("SELECT * FROM entrenador WHERE id = %s",(id,))
        return cursor.fetchone()
    
    @staticmethod
    @conn_cursor
    def crear_entrenador(cursor,trainer:dict)->int|None:
        
        cursor.execute("INSERT INTO entrenador (nombre,email,telefono) VALUES (%(nombre)s, %(email)s , %(telefono)s) RETURNING id",trainer)
        id_trainer = cursor.fetchone()
        return id_trainer
    
    @staticmethod
    @conn_cursor
    def actualizar_entrenador(cursor,trainer:dict)->bool:
        
        cursor.execute("UPDATE entrenador SET nombre=%(nombre)s,email=%(email)s,telefono=%(telefono)s WHERE id = %(id)s",trainer)
        if cursor.rowcount > 0:
            return True
        return False
       
    @staticmethod 
    @conn_cursor
    def eliminar_entrenador(cursor,id:int)->bool:
        cursor.execute("DELETE FROM entrenador WHERE id = %s",(id,))
        if cursor.rowcount > 0:
            return True
        return False