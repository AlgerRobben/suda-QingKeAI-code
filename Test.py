from PySide2.QtWidgets import QApplication, QWidget
import interface

app = QApplication([])

mainWindow = QWidget()

ui = interface.Ui_Form()

ui.setupUi(mainWindow)

mainWindow.showMaximized()

app.exec_()

