import os
import sys
import ctypes

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QIcon


class MLineEdit(QTextEdit):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.svg_list = None

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.svg_list = []
        filePathList = e.mimeData().text()
        filePath = filePathList.split('\n')
        files = ''
        for file in filePath:
            if file != '':
                file = file.replace('file:///', '', 1)
                files += file + '\n'
                self.svg_list.append(file)
        self.setText(files)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 596)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = MLineEdit('', self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 787, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.set_action()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SVG2PDF Tool alpha"))
        self.pushButton.setText(_translate("MainWindow", "Trans."))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def set_action(self):
        self.pushButton.clicked.connect(self.svg2pdf)

    def svg2pdf(self):
        pdf_filename = ''
        for i, svg_file in enumerate(self.textEdit.svg_list):
            root = os.path.dirname(svg_file)
            pdf_file = root + '/' + os.path.basename(svg_file).replace('.svg', '.pdf')
            pdf_filename += pdf_file + '\n'
            renderPDF.drawToFile(svg2rlg(svg_file), pdf_file)
            bar1 = '|' + '>' * (i+1) + '-' * (len(self.textEdit.svg_list)-i-1) + '|'
            self.textEdit_2.setText(bar1)
            QtWidgets.QApplication.processEvents()
        self.textEdit_2.setText(pdf_filename + 'Done!')


def show_win():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    main_window = QtWidgets.QMainWindow()
    ui.setupUi(main_window)
    main_window.setWindowIcon(QIcon('./T.ico'))

    ac_exit = ui.actionExit

    def exit_app():
        app.quit()
    ac_exit.triggered.connect(exit_app)

    main_window.show()
    sys.exit((app.exec_()))


if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    show_win()
