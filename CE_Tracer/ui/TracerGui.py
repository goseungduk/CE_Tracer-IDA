from os.path import dirname, abspath
import os
import idaapi
from CE_Tracer.ui.helpers.QtCollect import QtCollection

class TracerGui(idaapi.PluginForm):
    def __init__(self):
        super(TracerGui,self).__init__()
        ''' IDAGui() No arguments '''
        self.qc = QtCollection()
        self.icon = self.qc.QtGui.QIcon(dirname(abspath(__file__))+"\\icon.png")

    def setupControlPanel(self):
        self.text_widget = self.qc.QLineEdit()
        self.first_scan = self.qc.QPushButton("First Scan")
        self.next_scan = self.qc.QPushButton("Next Scan")
        button_layout = self.qc.QHBoxLayout()
        button_layout.setSpacing(50)
        button_layout.addWidget(self.first_scan)
        button_layout.addWidget(self.next_scan)
        layout = self.qc.QVBoxLayout()
        button_layout.setAlignment(self.qc.Qt.AlignTop) # button layout is placed on the top
        layout.addLayout(button_layout)
        layout.addWidget(self.text_widget)
        layout.addStretch() # text widget is placed under the button layout
        return layout

    def setupLayout(self):
        self.tableWidget = self.qc.QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(100)
        self.tableWidget.setHorizontalHeaderLabels(["Address","Value","Prev Value"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.qc.QHeaderView.Stretch)

        layout = self.qc.QHBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addLayout(self.setupControlPanel())
        self.parent.setLayout(layout)

    def OnCreate(self, form):
        self.parent = self.FormToPyQtWidget(form)
        self.parent.setWindowIcon(self.icon)
        self.setupLayout()

    def Show(self):
        name = "CE Tracer"
        try:
            options = idaapi.PluginForm.WCLS_CLOSE_LATER |\
                    idaapi.PluginForm.WCLS_SAVE |\
                    idaapi.PluginForm.WOPN_RESTORE
        except:
            options = idaapi.PluginForm.FORM_CLOSE_LATER |\
                        idaapi.PluginForm.FORM_SAVE |\
                        idaapi.PluginForm.FORM_RESORE
        return idaapi.PluginForm.Show(self, name, options=options)