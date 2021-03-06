from os.path import dirname, abspath
import idaapi, idc
from CE_Tracer.ui.helpers.QtCollect import QtCollection
from CE_Tracer.core.Scan import Scanner

class TracerGui(idaapi.PluginForm):
    def __init__(self):
        super(TracerGui,self).__init__()
        self.qc = QtCollection()
        self.icon = self.qc.QtGui.QIcon(dirname(abspath(__file__))+"\\icon.png")

    def first_scan_event(self):
        if(self.text_widget.text()==""):
            idc.warning("Type any value in text box")
            return
        self.tableWidget.setRowCount(0)
        self.byte_split = self.bytes_combo.currentText().split(" ")[0]
        self.scanner = Scanner()
        self.scanner.do_scan(self.text_widget.text(), self.byte_split)
        for r in self.scanner.scan_res:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, self.qc.QTableWidgetItem(str(r["name"])))
            self.tableWidget.setItem(rowPosition, 1, self.qc.QTableWidgetItem(hex(r["addr"])))
            self.tableWidget.setItem(rowPosition, 2, self.qc.QTableWidgetItem(str(r["value"])))
            self.tableWidget.setItem(rowPosition, 3, self.qc.QTableWidgetItem(str(r["prev"])))

    def next_scan_event(self):
        if(self.text_widget.text()==""):
            idc.warning("Type any value in text box")
            return
        self.scanner.next_scan(self.text_widget.text(), self.byte_split)
        self.tableWidget.setRowCount(0)
        for r in self.scanner.scan_res:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, self.qc.QTableWidgetItem(str(r["name"])))
            self.tableWidget.setItem(rowPosition, 1, self.qc.QTableWidgetItem(hex(r["addr"])))
            self.tableWidget.setItem(rowPosition, 2, self.qc.QTableWidgetItem(str(r["value"])))
            self.tableWidget.setItem(rowPosition, 3, self.qc.QTableWidgetItem(str(r["prev"])))

    def setupControlPanel(self):
        # Text Field
        self.text_widget = self.qc.QLineEdit()
        # Scan Button
        self.first_scan = self.qc.QPushButton("First Scan")
        self.first_scan.clicked.connect(self.first_scan_event)
        self.next_scan = self.qc.QPushButton("Next Scan")
        self.next_scan.clicked.connect(self.next_scan_event)
        # Value Type
        self.bytes_combo = self.qc.QComboBox()
        self.bytes_combo.addItems(["1 byte", "4 bytes", "8 bytes"])
        self.bytes_combo.insertSeparator(1)
        self.bytes_combo.insertSeparator(2)
        self.bytes_combo.setCurrentIndex(3)
        button_layout = self.qc.QHBoxLayout()
        button_layout.setSpacing(50)
        button_layout.addWidget(self.first_scan)
        button_layout.addWidget(self.next_scan)
        layout = self.qc.QVBoxLayout()
        button_layout.setAlignment(self.qc.Qt.AlignTop) # button layout is placed on the top
        layout.addLayout(button_layout)
        layout.addWidget(self.text_widget)
        layout.addWidget(self.bytes_combo)
        layout.addStretch() # text widget is placed under the button layout
        return layout

    def setupLayout(self):
        self.tableWidget = self.qc.QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Section","Address","Value","Prev Value"])
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