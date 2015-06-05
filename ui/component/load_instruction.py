# -*- coding: cp936 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
sys.path.append('C:\\Users\\You\\Documents\\GitHub\\AE86\\accessory')
from load_yo import load_yo

def load_instruction(self):
    file_name = QtGui.QFileDialog.getOpenFileName(self, self.tr('Open instruction file'), QtCore.QString())
    load_yo(file_name)
    QtGui.QMessageBox.information(self, "It works!", u"成功载入汇编文件%s" % file_name)