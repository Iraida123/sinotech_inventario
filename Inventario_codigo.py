
import sqlite3
DBName = "inventario.db"
conexion=sqlite3.connect(DBName)
cursor=conexion.cursor()
opcion=0




def mostrar_menu():               #Defino la funcion para mostrar el menu
    print("")
    print("***Bienveido al sistema de inventario SINOTECH. Ingrese una opcion para continuar \n")
    print("-----MENU PRINCIPAL-----")
    print("1. Dar Alta a Nuevo producto ")
    print("2. Mostrar lista de productos")
    print("3. Actualizar Producto")
    print("4. Dar de baja producto")
    print("5. Buscar Producto")
    print("6. Reporte de Bajo stock")
    print("7. Salir")
    

def create_table_materiales():
        
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materiales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- ID único para cada producto
    nombre VARCHAR(255) NOT NULL,              -- Nombre del producto
    descripcion TEXT,                          -- Descripción del producto
    stock  INT NOT NULL DEFAULT 0,           -- Cantidad disponible del producto
    precio DECIMAL(10, 2) NOT NULL,            -- Precio del producto
    categoria VARCHAR(255)                    -- Categoría del producto
    )
    """
    )
    conexion.commit()
    # Cerrar la conexión
    
    

#defino la funcion ingresar producto
def insert_producto():
    print("\nAgregar Nuevo Producto:")   
         
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción del producto: ")
    stock = int(input("Cantidad disponible: "))
    precio = float(input("Precio del producto: "))
    categoria = input("Categoría del producto: ")

    with sqlite3.connect(DBName) as conexion:    
        cursor=conexion.cursor()  

        query = ("INSERT INTO materiales (nombre, descripcion, stock, precio, categoria) VALUES (?,?, ?,? ,?)")
        values = (nombre, descripcion, stock, precio, categoria)

        cursor.execute(query, values)
        conexion.commit()

    print(f"\nProducto '{nombre}' agregado exitosamente.")
    
    cursor.close()
    conexion.close()    
   



def mostrar_productos():
    conexion = sqlite3.connect(DBName)
    cursor = conexion.cursor()

    # Ejecutar la consulta SELECT y obtener todos los registros
    query = "SELECT * FROM materiales"
    cursor.execute(query)
    productos = cursor.fetchall()
    
    # Mostrar los resultados
    if productos:
        print("\nID | Nombre | Descripción | Stock | Precio | Categoría")
        for producto in productos:
            id_producto, nombre, descripcion, stock, precio, categoria = producto
            print(f"{id_producto} | {nombre} | {descripcion} | {stock} | {precio} | {categoria}")
    else:
        print("No hay productos registrados.")

     
    

def actualizar_producto():
    #  Permite actualizar la cantidad de un producto específico.
    print("\nActualizar Producto:")
    id_producto = int(input("ID del producto a actualizar: "))
    nueva_cantidad = int(input("Nueva cantidad disponible: "))

    conexion=sqlite3.connect(DBName)
    cursor=conexion.cursor()
    query = "UPDATE materiales SET stock = ? WHERE id =? "
    values = (nueva_cantidad, id_producto)

    cursor.execute(query, values)
    conexion.commit()

    if cursor.rowcount > 0:
        print(f"\nProducto con ID {id_producto} actualizado exitosamente.")
    else:
        print( f"No se encontró un producto con el ID {id_producto}.")

    conexion.commit()    
    conexion.close()


def eliminar_producto():
   
    #Elimina un producto del inventario utilizando su ID.
    
    print("\nEliminar Producto:")
    id_producto = int(input("ID del producto a eliminar: "))

    conexion=sqlite3.connect(DBName)
    cursor=conexion.cursor()
    
    query = "DELETE FROM materiales WHERE id = ? "
    values = (id_producto,)

    cursor.execute(query, values)
    conexion.commit()

    if cursor.rowcount > 0:
        print(f"\nProducto con ID {id_producto} eliminado exitosamente.")
    else:
        print(f"No se encontró un producto con el ID {id_producto}.")

    conexion.commit()    
    cursor.close()
    conexion.close()

def buscar_producto():
    #Permite buscar productos por ID, nombre o categoría.

    print("\nBuscar Producto:")
    opcion = input("Buscar por (1) ID, (2) Nombre, (3) Categoría: ")

    conexion=sqlite3.connect(DBName)
    cursor=conexion.cursor()
    if opcion == "1":
        id_producto = int(input("ID del producto a buscar: "))
        query = "SELECT * FROM materiales WHERE id = ?"
        values = (id_producto,)
    elif opcion == "2":
        nombre = input("Nombre del producto a buscar: ")
        query = "SELECT * FROM materiales WHERE nombre LIKE ?"
        values = (f"%{nombre}%",)
    elif opcion == "3":
        categoria = input( "Categoría del producto a buscar: ")
        query = "SELECT * FROM productos WHERE categoria LIKE ? "
        values = (f"%{categoria}%", )

    else:
        print("Opción inválida.")
        cursor.close()
        conexion.close()
        return

    cursor.execute(query, values)
    materiales = cursor.fetchall()

    if materiales:
        print("\nID | Nombre | Descripción | stock | Precio | Categoría")
        for producto in materiales:
            print(f"{producto[0]} | {producto[1]} | {producto[2]} | {producto[3]} | {producto[4]} | {producto[5]}")
    else:
        print("No se encontraron productos que coincidan con la búsqueda.")

    cursor.close()
    conexion.close()




def reporte_bajo_stock():
    
   # Muestra un reporte de productos con cantidad menor o igual al límite especificado por el usuario.
    
    limite = int(input("Ingrese el límite de stock: "))

    conexion=sqlite3.connect(DBName)
    cursor=conexion.cursor()

    query = "SELECT * FROM materiales WHERE cantidad <= ?"
    values = (limite,)
    cursor.execute(query, values)

    materiales = cursor.fetchall()

    if materiales:
        print("\nID | Nombre | Descripción | Cantidad | Precio | Categoría")
        for producto in materiales:
            print(f"{producto[0]} | {producto[1]} | {producto[2]} | {producto[3]} | {producto[4]} | {producto[5]}")
    else:
        print("No hay productos con bajo stock.")

    cursor.close()
    conexion.close()

def dato_producto():
    
    

while opcion != 7:
    mostrar_menu() 
    opcion = int(input("Introduzca una opcion (1-7) para continuar:"))
    if opcion == 1:
        insert_producto()
    elif opcion == 2:        
        mostrar_productos()
    elif opcion == 3:
        actualizar_producto()
    elif opcion == 4:
        
        eliminar_producto()
    elif opcion == 5:
        buscar_producto()
    elif opcion == 6:
        reporte_bajo_stock()
    elif opcion == 7:
        print("---Usted a seleccionado salir del programa, Hasta luego.....")
        #break # solo si usamos un while true
    else:
        print("Opción inválida. Intente nuevamente.")
        



