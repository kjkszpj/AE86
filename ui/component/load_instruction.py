# -*- coding: cp936 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from load_yo import load_yo


def load_instruction(ui):
    file_name = QtGui.QFileDialog.getOpenFileName(ui, ui.tr('Open instruction file'), "", QtCore.QString('*.yo'))
    load_yo(file_name)
    QtGui.QMessageBox.information(ui, "It works!", u"成功载入汇编文件%s" % file_name)
