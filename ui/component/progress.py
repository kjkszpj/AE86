# -*- coding: cp936 -*-

from pickle import load
from pickle import dump
from PyQt4 import QtCore
from PyQt4 import QtGui
import memory


def load_progress(parent):
    file_name = QtGui.QFileDialog.getOpenFileName(parent, u'�򿪽����ļ�', '', QtCore.QString('*.pk'))
    memory.mem = load(file(file_name, 'r'))
    QtGui.QMessageBox.information(parent, "It works!", u"�ɹ���������ļ� %s" % file_name)


def save_progress(parent):
    file_name = QtGui.QFileDialog.getSaveFileName(parent, u'��������ļ�', '', QtCore.QString('*.pk'))
    dump(memory.mem, file(file_name, 'w'))
    QtGui.QMessageBox.information(parent, "It works!", u"�ɹ����浽%s" % file_name)