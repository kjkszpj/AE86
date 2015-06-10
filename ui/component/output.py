# -*- coding: cp936 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore


def output(widow):
    output_file_name = QtGui.QFileDialog.getSaveFileName(widow, u'导出结果', '', QtCore.QString('*.txt'))
    widow.sim.run_all(file_name = output_file_name)
    QtGui.QMessageBox.information(widow, "It works!", u"成功导出结果到 %s" % output_file_name)
