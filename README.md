# Inventario by ADM
# Clase `MainWindow` - Explicación Detallada

La clase `MainWindow` extiende de `QMainWindow` y sirve como la ventana principal de una aplicación basada en PySide6. A continuación, se describen los aspectos más relevantes de su funcionalidad y estructura.

---

## Inicialización

### Constructor `__init__`
1. **Carga de interfaz gráfica**:
   - Utiliza un archivo `.ui` llamado `setup.ui` para configurar la interfaz.
   - Maneja posibles errores al abrir el archivo.
   - Usa `QtUiTools.QUiLoader` para cargar la interfaz.

2. **Configuraciones iniciales**:
   - Conecta múltiples botones a sus respectivas funciones usando `clicked.connect`.
   - Establece la ventana como **sin bordes** con `QtCore.Qt.FramelessWindowHint`.
   - Agrega un grip para redimensionar la ventana y lo posiciona dinámicamente en el evento de redimensionamiento (`resizeEvent`).

---

## Funcionalidades Principales

### Gestión de Botones y Navegación
- **Minimizar, maximizar y restaurar**:
  - `control_bt_minimizar`: Minimiza la ventana.
  - `control_bt_maximizar`: Maximiza la ventana.
  - `control_bt_normal`: Restaura la ventana a su tamaño normal.

- **Cambio entre páginas del `stackedWidget`**:
  - Los botones como `bt_database`, `bt_registrar`, `bt_actualizar` y `bt_eliminar` permiten la navegación entre distintas páginas de la interfaz.

- **Menú lateral animado**:
  - La función `mover_menu` controla la animación de mostrar u ocultar el menú lateral usando `QPropertyAnimation`.

---

### Funciones Relacionadas con Productos

#### Mostrar Productos
- **`mostrar_productos`**: 
  - Obtiene los datos desde la base de datos (`Comunicacion`) y los muestra en una tabla (`tablaProductos`).
  - Limpia los mensajes de señal para evitar confusión.

- **`mostrar_productos_eliminar`**: 
  - Similar a `mostrar_productos`, pero enfocado en una tabla específica (`tablaBorrar`) para eliminación.

#### Registrar Productos
- **`registrar_productos`**:
  - Valida la entrada del usuario (nombres, cantidades y precios).
  - Verifica si el producto ya existe en la base de datos.
  - Registra un nuevo producto si no existe y limpia los campos del formulario.

#### Buscar Productos
- **`buscar_por_nombre_actualiza`**: 
  - Busca un producto por nombre y modelo para actualizarlo.
  - Si se encuentra, rellena los campos de edición.

- **`buscar_por_nombre_borrar`**:
  - Busca productos para eliminarlos y los muestra en la tabla correspondiente.

- **`buscar_por_nombre_db`**:
  - Similar a las anteriores, pero muestra los productos en la tabla principal.

#### Modificar Productos
- **`modificar_productos`**:
  - Actualiza la información de un producto existente.
  - Limpia los campos del formulario tras la actualización.

#### Eliminar Productos
- **`eliminar_productos`**:
  - Elimina un producto basado en su nombre y modelo.
  - Refresca la tabla tras la eliminación.

#### Otras Funciones Relacionadas
- **`cargar_producto_seleccionado`**:
  - Obtiene los datos de un producto seleccionado en la tabla para su eliminación.

- **`restar_cantidad`**:
  - Maneja una acción al hacer doble clic en una celda específica para modificar cantidades.

---

## Eventos Personalizados

### Redimensionamiento
- **`resizeEvent`**:
  - Ajusta dinámicamente la posición del grip de redimensionamiento.

### Movimiento de Ventana
- **`mousePressEvent` y `mouseMoveEvent`**:
  - Permiten mover la ventana al hacer clic y arrastrar en el área superior (`frame_superior`).

---

## Interacción con la Base de Datos

La clase utiliza una instancia de `Comunicacion` para gestionar la conexión con la base de datos. Las operaciones incluyen:
- Mostrar productos (`mostrar_producto`).
- Insertar productos (`inserta_producto`).
- Consultar productos existentes (`consultar_producto`).
- Actualizar y eliminar productos (`actualiza_producto` y `elimina_producto`).

---

## Resumen

La clase `MainWindow` es un componente completo para gestionar una aplicación de inventarios con las siguientes características:
- **Interfaz gráfica personalizable** (sin bordes y con animaciones).
- **Gestión de productos** (registro, búsqueda, actualización y eliminación).
- **Navegación fluida** entre secciones.
- **Optimización para eventos del sistema** (movimiento y redimensionamiento).

Este diseño proporciona una base sólida y extensible para agregar nuevas funcionalidades en el futuro.
