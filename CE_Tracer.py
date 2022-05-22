import idaapi
from PyQt5 import QtGui
from CE_Tracer.ui.TracerGui import TracerGui

class CE_Tracer(idaapi.plugin_t):
    flags = idaapi.PLUGIN_PROC
    comment = "CE Tracer"
    help = "CE Tracer"
    wanted_name = "CE Tracer"
    wanted_hotkey = "Shift+T"

    def init(self):
        return idaapi.PLUGIN_KEEP
    def term(self):
        pass
    def run(self, arg):
        form = TracerGui()
        form.Show()
        return

def PLUGIN_ENTRY():
    return CE_Tracer()
