# -*- coding: utf-8 -*-
import os

import sys
from PyQt4 import QtCore, QtGui
from clients.test_ui import *
from lines_provider import *
import md5

def get_line(line_address):
    line_data = "0x%x"%line_address
    line_data += md5.md5(line_data).hexdigest()
    return line_data

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_Form()
        lines_provider = DisassembleLinesProvider2(MockDisassemblerInterface())
        self.ui.setupUi(self)
        self.ui.memory_text.init(lines_provider)
        #print "here"
        #self.min_max_changed("")
        #QtCore.QObject.connect(self.ui.min_addr, QtCore.SIGNAL("textChanged(QString)"), self.min_max_changed)
        #QtCore.QObject.connect(self.ui.max_addr, QtCore.SIGNAL("textChanged(QString)"), self.min_max_changed)
        #self.ui.button_save.setEnabled(False)
        #QtCore.QObject.connect(self.ui.button_open,QtCore.SIGNAL("clicked()"), self.file_dialog)
        #QtCore.QObject.connect(self.ui.button_save,QtCore.SIGNAL("clicked()"), self.file_save)
        #QtCore.QObject.connect(self.ui.editor_window,QtCore.SIGNAL("textChanged()"), self.enable_save)


    def min_max_changed(self, string):
        self.ui.memory_text.setMinimum(self.ui.min_addr.text().toInt(16)[0])
        self.ui.memory_text.setMaximum(self.ui.max_addr.text().toInt(16)[0])


    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.filename):
            import codecs
            s = codecs.open(self.filename,'r','utf-8').read()
            self.ui.editor_window.setPlainText(s)
            # inserting text emits textChanged() so we disable the button :)
            self.ui.button_save.setEnabled(False)
    def enable_save(self):
        self.ui.button_save.setEnabled(True)
    def file_save(self):
        from os.path import isfile
        if isfile(self.filename):
            import codecs
            s = codecs.open(self.filename,'w','utf-8')
            s.write(unicode(self.ui.editor_window.toPlainText()))
            s.close()
            self.ui.button_save.setEnabled(False)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())