import sqlite3

class Comunicacion():
    def __init__(self):
        self.con = sqlite3.connect('inventory_control.db')
    
    def inserta_producto(self, nombre, modelo, cantidad, precio, desc):
        cursor = self.con.cursor()
        query = '''INSERT INTO control (nombre, modelo, cantidad, precio, descripcion) VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(nombre, modelo, cantidad, precio, desc)
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def mostrar_producto(self):
        cursor = self.con.cursor()
        query = 'SELECT * FROM control'
        cursor.execute(query)
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    def busca_producto(self, nombre_producto=None, modelo_producto=None):
        try:
            cursor = self.con.cursor()
            if nombre_producto and modelo_producto:
                query = "SELECT * FROM control WHERE nombre = ? AND modelo = ?"
                cursor.execute(query, (nombre_producto, modelo_producto))
            elif nombre_producto:
                query = "SELECT * FROM control WHERE nombre = ?"
                cursor.execute(query, (nombre_producto,))
            elif modelo_producto:
                query = "SELECT * FROM control WHERE modelo = ?"
                cursor.execute(query, (modelo_producto,))
            else:
                return None  # No se especificó ningún filtro

            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except sqlite3.OperationalError as e:
            print(f"Error en la consulta SQL: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None



    
    def elimina_producto(self, nombre_producto, modelo_producto):
        cursor = self.con.cursor()
        try:
            query = 'DELETE FROM control WHERE nombre = ? and modelo = ?'
            cursor.execute(query, (nombre_producto, modelo_producto))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar el producto: {e}")
            raise e
        finally:
            cursor.close()


    def actualiza_producto(self, Id, nombre, modelo, cantidad, precio, desc):
        cursor = self.con.cursor()
        query = '''UPDATE control SET nombre = '{}', modelo = '{}', precio = '{}', cantidad = '{}', descripcion = '{}' WHERE ID = '{}' '''.format(nombre, modelo, precio, cantidad, desc, Id)
        cursor.execute(query)
        a = cursor.rowcount
        self.con.commit()
        cursor.close()
        return a
    
    def consultar_producto(self, nombre, modelo):
        cursor = self.con.cursor()
        query = f"SELECT * FROM control WHERE nombre = '{nombre}' AND modelo = '{modelo}'"
        result = cursor.execute(query).fetchall()
        cursor.close()
        return result 
    
    def actualiza_producto_cantidad(self, nombre, modelo, nueva_cantidad):
        try:
            cursor = self.con.cursor()
            query = 'UPDATE control SET cantidad = ? WHERE nombre = ? AND modelo = ?'
            cursor.execute(query, (nueva_cantidad, nombre, modelo))
            self.con.commit()
            cursor.close()
        except sqlite3.OperationalError as e:
            print(f"Error SQLite al actualizar cantidad: {e}")
        except Exception as e:
            print(f"Error inesperado al actualizar cantidad: {e}")

    def actualiza_producto_descripcion(self, nombre, modelo, nueva_descripcion):
        try:
            cursor = self.con.cursor()
            query = 'UPDATE control SET descripcion = ? WHERE nombre = ? AND modelo = ?'
            cursor.execute(query, (nueva_descripcion, nombre, modelo))
            self.con.commit()
            cursor.close()
        except sqlite3.OperationalError as e:
            print(f"Error SQLite al actualizar cantidad: {e}")
        except Exception as e:
            print(f"Error inesperado al actualizar cantidad: {e}")

