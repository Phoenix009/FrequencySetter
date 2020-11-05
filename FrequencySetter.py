from PySide2 import QtCore, QtGui, QtWidgets
from serial.tools.list_ports import comports
from SerialPort import SerialPort


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.frequencies = ['402', '403', '404', '405']

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 250)
        MainWindow.setMinimumSize(QtCore.QSize(630, 250))
        MainWindow.setMaximumSize(QtCore.QSize(630, 250))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(600, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setMinimumSize(QtCore.QSize(600, 0))
        self.title.setMaximumSize(QtCore.QSize(600, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout_3.addWidget(self.title)
        self.message = QtWidgets.QLabel(self.centralwidget)
        self.message.setText("")
        self.message.setObjectName("messageself.message")
        self.verticalLayout_3.addWidget(self.message)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.choose_port_label = QtWidgets.QLabel(self.centralwidget)
        self.choose_port_label.setMinimumSize(QtCore.QSize(300, 0))
        self.choose_port_label.setMaximumSize(QtCore.QSize(300, 16777215))
        self.choose_port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.choose_port_label.setObjectName("choose_port_label")
        self.verticalLayout_2.addWidget(self.choose_port_label)
        self.port_selection = QtWidgets.QComboBox(self.centralwidget)
        self.port_selection.setMinimumSize(QtCore.QSize(300, 0))
        self.port_selection.setMaximumSize(QtCore.QSize(300, 16777215))
        self.port_selection.setObjectName("port_selection")
        self.port_selection.addItem("")
        self.verticalLayout_2.addWidget(self.port_selection)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.choose_frequency_label = QtWidgets.QLabel(self.centralwidget)
        self.choose_frequency_label.setMinimumSize(QtCore.QSize(300, 0))
        self.choose_frequency_label.setMaximumSize(QtCore.QSize(300, 16777215))
        self.choose_frequency_label.setAlignment(QtCore.Qt.AlignCenter)
        self.choose_frequency_label.setObjectName("choose_frequency_label")
        self.verticalLayout.addWidget(self.choose_frequency_label)
        self.frequency_selection = QtWidgets.QComboBox(self.centralwidget)
        self.frequency_selection.setMinimumSize(QtCore.QSize(300, 0))
        self.frequency_selection.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frequency_selection.setObjectName("frequency_selection")
        self.frequency_selection.addItem("")
        self.verticalLayout.addWidget(self.frequency_selection)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.change_frequency = QtWidgets.QPushButton(self.centralwidget)
        self.change_frequency.setMinimumSize(QtCore.QSize(600, 30))
        self.change_frequency.setMaximumSize(QtCore.QSize(610, 16777215))
        self.change_frequency.setObjectName("change_frequency")
        self.verticalLayout_3.addWidget(self.change_frequency)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 630, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "Frequency Setter"))
        self.choose_port_label.setText(_translate("MainWindow", "Choose Port"))
        self.choose_frequency_label.setText(_translate("MainWindow", "Choose Frequency"))
        self.change_frequency.setText(_translate("MainWindow", "Change Frequency"))

        self.port_selection.addItems(self.get_comport_list())
        self.frequency_selection.addItems(self.frequencies)
        self.change_frequency.clicked.connect(self.change_frequency_init)

    def get_comport_list(self):
        comport_list = comports()
        comport_list = list(map(lambda x: str(x).split()[0], comport_list))
        return comport_list
    
    def change_frequency_init(self):
        port_name = self.port_selection.currentText()
        frequency = self.frequency_selection.currentText()
        self.message.setText("Setting Up Port {}".format(port_name))
        port = SerialPort(port_name)

        port.write_port("RadiosondeDAS")

        self.message.setText("Waiting for Response")
        while port.read_port() != "RadiosondeDAS": pass
        port.write_port(frequency)

        while port.read_port() != frequency: pass
        self.message.setText("Frequency Set: {}".format(frequency))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
