from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class QMemoryTextBox(QtGui.QTextEdit):
    def __init__(self, form):
        QtGui.QTextEdit.__init__(self, form)
        self.scroll_bar = QtGui.QScrollBar(form)
        self.form = form

    def init(self, lines_provider):
        self.lines_provider = lines_provider

        #self.setVerticalScrollBar(self.scroll_bar)

        self.setMinimum(0)
        self.setMaximum(self.lines_provider.get_num_of_lines())
        self.setPlainText("");
        #self.scroll_bar.setOrientation(QtCore.Qt.Vertical)
        #self.scroll_bar.setObjectName(_fromUtf8("scroll_bar"))
        self.scroll_bar.valueChanged.connect(self.value_change)
        self.prev_value = self.scroll_bar.value()
        self.first_line_id, self.first_line_text = self.lines_provider.get_line_from_line_number(0)

        self.update_lines()
    def value_change(self):
        if self.scroll_bar.value() == self.prev_value:
            return
        if self.scroll_bar.value() == self.prev_value+1:
            self.prev_value += 1
            self.first_line_id, self.first_line_text = self.lines_provider.get_next_line(self.first_line_id)
        elif self.scroll_bar.value() == self.prev_value-1:
            self.prev_value -= 1
            self.first_line_id, self.first_line_text = self.lines_provider.get_previous_line(self.first_line_id)
        else:
            self.prev_value = self.scroll_bar.value()
            self.first_line_id, self.first_line_text = self.lines_provider.get_line_from_line_number(self.prev_value)
        self.update_lines()


    def update_lines(self):
        lines = []
        text = self.first_line_text
        id = self.first_line_id
        for i in xrange(self.num_lines):
            lines.append(text)
            id, text = self.lines_provider.get_next_line(id)
        self.setPlainText("\n".join(lines))
        if self.lines_provider == None:
            return



    def setGeometry(self, args):
        QtGui.QTextEdit.setGeometry(self, args)
        # Set the scrollbar geometry:
        x, y, w, h = self.geometry().getRect()
        self.scroll_bar.setGeometry(x + w - 16, y, 16, h)

    def setMinimum(self, minimum):
        self.scroll_bar.setMinimum(minimum)
        self.update_scroll_visible()

    def update_scroll_visible(self):
        #return
        if self.scroll_bar.minimum() >= self.scroll_bar.maximum():
            if self.scroll_bar.isVisible():
                self.scroll_bar.setVisible(False)
                cur = self.geometry()
                cur.setWidth(cur.width() + 16)
                QtGui.QTextEdit.setGeometry(self, cur)
        else:
            if not self.scroll_bar.isVisible():
                self.scroll_bar.setVisible(True)
                cur = self.geometry()
                cur.setWidth(cur.width() - 16)
                QtGui.QTextEdit.setGeometry(self, cur)

    def setMaximum(self, maximum):
        self.num_lines = (self.height()-32) / self.fontMetrics().height()
        self.scroll_bar.setMaximum(maximum - self.num_lines)
        assert self.scroll_bar.maximum() == (maximum - self.num_lines), (self.scroll_bar.maximum() , (maximum - self.num_lines))
        self.update_scroll_visible()
