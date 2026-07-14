from database import conn_cursor

class UsuarioRepository:
    
    @staticmethod
    @conn_cursor
    def obtener_usuarios(cursor,nombre:str|None = None)->dict|None:

        if nombre is None:
            cursor.execute("SELECT * FROM usuario")
            return cursor.fetchall()
        # Si hay filtros, realizamos la búsqueda
        cursor.execute("SELECT * FROM usuario WHERE nombre ILIKE %s",(f"%{nombre}%",))
        filtrados = cursor.fetchall()
        return filtrados

    @staticmethod    
    @conn_cursor   
    def obtener_usuario(cursor,id:int)->dict|None:
        cursor.execute("SELECT * FROM usuario WHERE id = %s",(id,))
        usuario =  cursor.fetchone()
        if  usuario:
            return usuario
        return None
    
    @staticmethod    
    @conn_cursor    
    def crear_usuario(cursor,user_data:dict)->dict|None:

            cursor.execute("INSERT INTO usuario (nombre,email,telefono) VALUES (%(nombre)s,%(email)s,%(telefono)s) RETURNING id", user_data)
            id_record =  cursor.fetchone()
            return id_record
        
    @staticmethod
    @conn_cursor    
    def actualizar_usuario(cursor,user_data:dict)->bool:
        
        cursor.execute("UPDATE usuario SET nombre = %(nombre)s, email = %(email)s, telefono = %(telefono)s WHERE id = %(id)s",user_data)
        
        if cursor.rowcount > 0:
            return True
        return False

    @staticmethod
    @conn_cursor
    def actualizar_patch_usuario(cursor,id:int,user_data:dict)->dict|None:
        if not user_data:
            # Retornamos el usuario tal como está sin tocar la BD
            cursor.execute("SELECT * FROM usuario WHERE id = %s", (id,))
            return cursor.fetchone()
        columnas_set = ", ".join([f"{campo} = %({campo})s" for campo in user_data.keys()])
        user_data["id"]= id
        
        cursor.execute(f"UPDATE usuario SET {columnas_set} WHERE id = %(id)s",user_data)

        
        if cursor.rowcount > 0:
            cursor.execute("SELECT * FROM usuario WHERE id = %s",(id,))
            return cursor.fetchone()
        return None

    @staticmethod
    @conn_cursor       
    def eliminar_usuario(cursor,id:int)->bool:
        
        cursor.execute("DELETE FROM usuario WHERE id = %s",(id,))
        
        if cursor.rowcount > 0:
            return True
        return False
