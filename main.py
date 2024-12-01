import sqlite3
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QFile, Qt, QModelIndex
from PySide6 import QtCore, QtWidgets
from PySide6 import QtUiTools
from sqlite import Comunicacion

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui_file = QFile("setup.ui")
        if not ui_file.open(QFile.ReadOnly):
            print(f"Error al cargar el archivo de interfaz: {ui_file.errorString()}")
            sys.exit(1)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.ui.bt_menu.clicked.connect(self.mover_menu)
        self.db = Comunicacion()
        self.fila_seleccionada = None

        self.ui.bt_achicar.hide()
        self.ui.bt_refrescar.clicked.connect(self.mostrar_productos)
        self.ui.bt_agregar.clicked.connect(self.registrar_productos)
        self.ui.bt_borrar.clicked.connect(self.eliminar_productos)
        self.ui.bt_actualizar_update.clicked.connect(self.modificar_productos)
        self.ui.bt_buscar_actualizar.clicked.connect(self.buscar_por_nombre_actualiza)
        self.ui.bt_buscar_eliminar.clicked.connect(self.buscar_por_nombre_borrar)
        self.ui.bt_buscar_db.clicked.connect(self.buscar_por_nombre_db)
        self.ui.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.ui.bt_achicar.clicked.connect(self.control_bt_normal)
        self.ui.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())
        self.ui.bt_volver_desc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_db))
        self.ui.bt_guardar_desc.clicked.connect(self.guardar_descripcion)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        self.ui.frame_superior.mouseMoveEvent = self.mouseMoveEvent
        self.ui.tablaBorrar.cellClicked.connect(self.cargar_producto_seleccionado)
        self.ui.tablaProductos.cellDoubleClicked.connect(self.restar_cantidad)
        self.ui.tablaProductos.doubleClicked.connect(self.double_click)

        self.ui.bt_database.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_db))
        self.ui.bt_database.clicked.connect(self.mostrar_productos)
        self.ui.bt_registrar.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_registrar))
        self.ui.bt_actualizar.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_actualizar))
        self.ui.bt_eliminar.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_eliminar))
        self.ui.bt_eliminar.clicked.connect(self.mostrar_productos_eliminar)
        self.ui.bt_ajustes.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_ajustes))

        self.ui.tablaBorrar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tablaProductos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        self.ui.bt_achicar.hide()
        self.ui.bt_maximizar.show()

    def control_bt_maximizar(self):
        self.showMaximized()
        self.ui.bt_achicar.show()
        self.ui.bt_maximizar.hide()

    def resizeEvent(self, event):
        rect = event.size()
        self.grip.move(rect.width() - self.gripSize, rect.height() - self.gripSize)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            rect = self.ui.frame_superior.rect()
            global_top_left = self.ui.frame_superior.mapToGlobal(rect.topLeft())
            global_rect = QtCore.QRect(global_top_left, rect.size())
            if global_rect.contains(event.globalPosition().toPoint()):
                self.click_position = event.globalPosition().toPoint()
                self.is_dragging = True
                event.accept()
            else:
                self.is_dragging = False

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            if self.isMaximized() == False:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self.move(self.pos() + event.globalPosition().toPoint() - self.click_position)
                    self.click_position = event.globalPosition().toPoint()

            if event.globalPosition().y() <= 10:
                self.showMaximized()
                self.ui.bt_achicar.show()
                self.ui.bt_maximizar.hide()
            else:
                self.showNormal()
                self.ui.bt_achicar.hide()
                self.ui.bt_maximizar.show()



    def mover_menu(self):
        if True:
            width = self.ui.frame_menu.width()
            normal = 0
            if width==0:
                extender = 200
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.ui.frame_menu, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QEasingCurve.InOutQuart)
            self.animacion.start()

    def mostrar_productos(self):
        datos = self.db.mostrar_producto()
        i = len(datos)
        self.ui.tablaProductos.setRowCount(i)
        tablerow = 0
        for row in datos:
            self.Id = row[0]
            self.ui.tablaProductos.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.ui.tablaProductos.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.ui.tablaProductos.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.ui.tablaProductos.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[4]))
            self.ui.tablaProductos.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[5]))
            tablerow += 1
            self.ui.signal_actualizar.setText("")
            self.ui.signal_registrar.setText("")
            self.ui.signal_eliminar.setText("")

    def mostrar_productos_eliminar(self):
        datos = self.db.mostrar_producto()
        i = len(datos)
        self.ui.tablaBorrar.setRowCount(i)
        tablerow = 0
        for row in datos:
            self.Id = row[0]
            self.ui.tablaBorrar.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.ui.tablaBorrar.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.ui.tablaBorrar.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.ui.tablaBorrar.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[4]))
            self.ui.tablaBorrar.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[5]))
            tablerow += 1
            self.ui.signal_actualizar.setText("")
            self.ui.signal_registrar.setText("")
            self.ui.signal_eliminar.setText("")

    def registrar_productos(self):
        nombre = self.ui.line_reg_nombre.text().strip().upper()
        modelo = self.ui.line_reg_modelo.text().strip().upper()
        cantidad = self.ui.line_reg_cantidad.text().strip()
        precio = self.ui.line_reg_precio.text().strip()
        descripcion = self.ui.line_reg_desc.text().strip().upper()
        
        try:
            cantidad = int(cantidad)
            precio = int(precio)
        except ValueError:
            self.ui.signal_registrar.setText('La cantidad y el precio deben ser números válidos')
            return

        if not (nombre and modelo):
            self.ui.signal_registrar.setText('Nombre y modelo son obligatorio')
            return

        try:
            producto_existente = self.db.consultar_producto(nombre, modelo)
            if producto_existente:
                self.ui.signal_registrar.setText('Producto ya existe')
            else:
                self.db.inserta_producto(nombre, modelo, cantidad, precio, descripcion)
                self.ui.signal_registrar.setText('Producto Registrado')

                self.ui.line_reg_nombre.clear()
                self.ui.line_reg_modelo.clear()
                self.ui.line_reg_cantidad.clear()
                self.ui.line_reg_precio.clear()
                self.ui.line_reg_desc.clear()

        except sqlite3.OperationalError as e:
            self.ui.signal_registrar.setText('Error en la base de datos')
            print(f"Error SQLite: {e}")
        except Exception as e:
            self.ui.signal_registrar.setText('Error inesperado')
            print(f"Error inesperado: {e}")


    def buscar_por_nombre_actualiza(self):
        nombre_producto = self.ui.line_nombre_actualizar.text().strip().upper()
        modelo_producto = self.ui.line_modelo_actualizar.text().strip().upper()

        if not nombre_producto or not modelo_producto:
            self.ui.signal_actualizar.setText('El nombre y el modelo son obligatorios')
            return

        self.producto = self.db.busca_producto(nombre_producto, modelo_producto)
        
        if self.producto: 
            self.Id = self.producto[0][0]
            self.ui.line_nombre_act.setText(self.producto[0][1])
            self.ui.line_modelo_act.setText(self.producto[0][2])
            self.ui.line_cant_act.setText(str(self.producto[0][4]))
            self.ui.line_precio_act.setText(str(self.producto[0][3]))
            self.ui.line_desc_act.setText(self.producto[0][5])
            self.ui.signal_actualizar.setText('Producto encontrado')
        else:
            self.ui.signal_actualizar.setText('Producto no encontrado')


    def modificar_productos(self):
        if self.producto != '':
            nombre = self.ui.line_nombre_act.text().upper()
            modelo = self.ui.line_modelo_act.text().upper()
            cantidad = self.ui.line_cant_act.text().upper()
            precio = self.ui.line_precio_act.text().upper()
            descripcion = self.ui.line_desc_act.text().upper()
            act = self.db.actualiza_producto(self.Id, nombre, modelo, cantidad, precio, descripcion)
            if act == 1:
                self.ui.signal_actualizar.setText('Producto Actualizado')
                self.ui.line_nombre_act.clear()
                self.ui.line_modelo_act.clear()
                self.ui.line_cant_act.clear()
                self.ui.line_precio_act.clear()
                self.ui.line_desc_act.clear()
                self.ui.line_nombre_actualizar.setText('')
                self.ui.line_modelo_actualizar.setText('')
            elif act == 0:
                self.ui.signal_actualizar.setText('Error')
            else:
                self.ui.signal_actualizar.setText('Producto no encontrado')

    def buscar_por_nombre_borrar(self):
        nombre_producto = self.ui.line_nombre_eliminar.text().strip().upper()
        modelo_producto = self.ui.line_modelo_eliminar.text().strip().upper()

        producto = self.db.busca_producto(nombre_producto, modelo_producto)

        if not producto:
            self.ui.signal_eliminar.setText('Producto no encontrado')
            return

        if not all(isinstance(row, (tuple, list)) and len(row) > 5 for row in producto):
            self.ui.signal_eliminar.setText('Formato de datos incorrecto')
            return

        self.ui.tablaBorrar.setRowCount(len(producto))
        self.ui.signal_eliminar.setText('Producto Seleccionado')

        for tablerow, row in enumerate(producto):
            for col in range(1, 6): 
                self.ui.tablaBorrar.setItem(tablerow, col - 1, QtWidgets.QTableWidgetItem(str(row[col])))

    def buscar_por_nombre_db(self):
        nombre_producto = self.ui.line_nombre_db.text().strip().upper()
        modelo_producto = self.ui.line_modelo_db.text().strip().upper()

        producto = self.db.busca_producto(nombre_producto, modelo_producto)

        if not producto:
            self.ui.signal_db.setText('Producto no encontrado')
            self.ui.tablaProductos.setRowCount(0)
            return

        if not all(isinstance(row, (tuple, list)) and len(row) > 5 for row in producto):
            self.ui.signal_db.setText('Formato de datos incorrecto')
            return

        self.ui.tablaProductos.setRowCount(len(producto))

        for tablerow, row in enumerate(producto):
            for col in range(1, 6):
                self.ui.tablaProductos.setItem(tablerow, col - 1, QtWidgets.QTableWidgetItem(str(row[col])))

        self.ui.signal_db.setText('Producto encontrado')



    def cargar_producto_seleccionado(self, row):
        nombre_producto = self.ui.tablaBorrar.item(row, 0).text()
        modelo_producto = self.ui.tablaBorrar.item(row, 1).text()
        self.ui.line_nombre_eliminar.setText(nombre_producto)
        self.ui.line_modelo_eliminar.setText(modelo_producto)


    def eliminar_productos(self):
        nombre_producto = self.ui.line_nombre_eliminar.text().upper()
        modelo_producto = self.ui.line_modelo_eliminar.text().upper()
        if nombre_producto.strip() and modelo_producto.strip():
            try:
                self.db.elimina_producto(nombre_producto, modelo_producto)
                self.ui.signal_eliminar.setText('Producto Eliminado')
                self.ui.line_nombre_eliminar.clear()
                self.ui.line_modelo_eliminar.clear()
                self.mostrar_productos_eliminar()
            except Exception as e:
                self.ui.signal_eliminar.setText(f"Error al eliminar: {str(e)}")
                print(f"Error al eliminar: {str(e)}")
        else:
            self.ui.signal_eliminar.setText('Por favor, ingrese un nombre válido para eliminar.')

    def restar_cantidad(self, row, column):
        match column:
            case 3:
                try:
                    nombre = self.ui.tablaProductos.item(row, 0).text()
                    modelo = self.ui.tablaProductos.item(row, 1).text()
                    cantidad_actual = int(self.ui.tablaProductos.item(row, 3).text())
                    nuevo_consumo, ok = QtWidgets.QInputDialog.getInt(
                        self, "Consumo", "Ingrese el número a restar:", 0, 0
                    )

                    if ok: 
                        nueva_cantidad = cantidad_actual - nuevo_consumo

                        if nueva_cantidad < 0:
                            QtWidgets.QMessageBox.warning(
                                self, "Alerta", "No tienes stock para ese consumo"
                            )
                            return

                        self.ui.tablaProductos.setItem(
                            row, 3, QtWidgets.QTableWidgetItem(str(nueva_cantidad))
                        )

                        self.db.actualiza_producto_cantidad(nombre, modelo, nueva_cantidad)
                        self.ui.signal_actualizar.setText('Cantidad actualizada correctamente')
                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Error", f"Ocurrió un error al procesar la cantidad: {str(e)}"
                    )
            case 4:
                try:
                    self.ui.signal_desc.setText('')
                    self.fila_seleccionada = row
                    descripcion_actual = self.ui.tablaProductos.item(row, 4).text()
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_descripcion)
                    self.ui.text_desc.setPlainText(descripcion_actual)
                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Error", f"No se pudo cargar la descripción: {str(e)}"
                    )
            case _:
                self.ui.signal_db.setText('Solo se puede modificar cantidad y descripción')

    def guardar_descripcion(self):
        try:
            if self.fila_seleccionada is None:
                QtWidgets.QMessageBox.warning(self, "Alerta", "No hay producto seleccionado.")
                return

            nueva_descripcion = self.ui.text_desc.toPlainText()
            row = self.fila_seleccionada
            self.ui.tablaProductos.setItem(row, 4, QtWidgets.QTableWidgetItem(nueva_descripcion))
            nombre = self.ui.tablaProductos.item(row, 0).text()
            modelo = self.ui.tablaProductos.item(row, 1).text()
            self.db.actualiza_producto_descripcion(nombre, modelo, nueva_descripcion)

            self.ui.signal_desc.setText("Descripción actualizada correctamente")
            self.fila_seleccionada = None
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo guardar la descripción: {str(e)}")


    def double_click(self, index: QModelIndex):
        if isinstance(index, QModelIndex):
            item = self.ui.tablaProductos.item(index.row(), index.column())
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        else:
            print("El índice no es válido.")



if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    mi_app = MainWindow()
    mi_app.show()
    sys.exit(app.exec())
            