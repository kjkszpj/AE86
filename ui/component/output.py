# -*- coding: cp936 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore


def output(widow):
    output_file_name = QtGui.QFileDialog.getSaveFileName(widow, u'�������', '', QtCore.QString('*.txt'))
    widow.sim.run_all(file_name = output_file_name)
    QtGui.QMessageBox.information(widow, "It works!", u"�ɹ���������� %s" % output_file_name)
