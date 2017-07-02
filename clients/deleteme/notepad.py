# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from edytor import Ui_notepad
import md5

def get_line(line_address):
    line_data = "0x%x"%line_address
    line_data += md5.md5(line_data).hexdigest()
    return line_data

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_notepad()
        self.ui.setupUi(self)

        self.min_max_changed("")
        QtCore.QObject.connect(self.ui.min_addr, QtCore.SIGNAL("textChanged(QString)"), self.min_max_changed)
        #self.ui.button_save.setEnabled(False)
        #QtCore.QObject.connect(self.ui.button_open,QtCore.SIGNAL("clicked()"), self.file_dialog)
        #QtCore.QObject.connect(self.ui.button_save,QtCore.SIGNAL("clicked()"), self.file_save)
        #QtCore.QObject.connect(self.ui.editor_window,QtCore.SIGNAL("textChanged()"), self.enable_save)


    def min_max_changed(self, string):
        print type(str(self.ui.max_addr.text()))
        self.ui.scroll_bar.setMinimum(int(self.ui.min_addr.text(),16))
        self.ui.scroll_bar.setMaximum(int(self.ui.max_addr.text(),16))


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