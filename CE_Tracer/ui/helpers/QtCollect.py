import CE_Tracer.ui.helpers.QtObjs as QtObjs

class QtCollection():
    def __init__(self):
        self.QtObjs = QtObjs
        self.QtGui = self.QtObjs.get_QtGui()
        self.QtCore = self.QtObjs.get_QtCore()
        self.Qt = self.QtObjs.get_Qt()
        self.QtWidgets = self.QtObjs.get_QtWidgets()
        self.QTableWidget = self.QtObjs.get_QTableWidget()
        self.QHeaderView = self.QtObjs.get_QHeaderView()
        self.QVBoxLayout = self.QtObjs.get_QVBoxLayout()
        self.QHBoxLayout = self.QtObjs.get_QHBoxLayout()
        self.QTextEdit = self.QtObjs.get_QTextEdit()
        self.QLineEdit = self.QtObjs.get_QLineEdit()
        self.QPushButton = self.QtObjs.get_QPushButton()
        self.QTableWidgetItem = self.QtObjs.get_QTableWidgetItem()
        self.QMessageBox = self.QtObjs.get_QMessageBox()