
import random

import sys
from PyQt5 import QtCore, QtSerialPort
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap

############################################
max_num = 3
############################################

star_x_position = (110, 290, 470, 650, 830, 1010, 1190, 1370, 1550, 1730)
star_y_position = 20
ql_x_position = (170, 410, 650, 170, 410, 650, 170, 410, 650)
qr_x_position = (1130, 1370, 1610, 1130, 1370, 1610, 1130, 1370, 1610)
q_y_position = (140, 140, 140, 280, 280, 280, 420, 420, 420)
a_x_position = (25, 175, 325, 475, 625, 775, 925, 1075, 1225, 1375, 25, 175, 325, 475, 625, 775, 925, 1075, 1225, 1375)
a_y_position = (740, 740, 740, 740, 740, 740, 740, 740, 740, 740, 890, 890, 890, 890, 890, 890, 890, 890, 890, 890)

image = QImage('donut.png').scaled(120,120,QtCore.Qt.KeepAspectRatio) 


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.question = True
        self.q1 = 0
        self.q2 = 0
        self.real_answer = 0
        self.start_button_ready = True
        self.answer_button_ready = False
        self.your_answer = 0
        self.ok_count = 0

    def initUI(self):
        
        self.donut_pixmap = QPixmap.fromImage(image)

        vbox = QVBoxLayout(self)
		
        layout = QGridLayout()

        self.star_label = [QLabel(self) for i in range(10)]
        
        for i in range(10):
            self.star_label[i].setFrameStyle(QFrame.Box | QFrame.Plain)
            self.star_label[i].setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(self.star_label[i], 0, i)
        

        top = QFrame()
        top.setFrameShape(QFrame.StyledPanel)
        
        top.setLayout(layout)

        main = QFrame()
        main.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)
        '''
        splitter1 = QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(top)
        splitter1.addWidget(main)

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        '''
#        splitter2.setSizes([100,100])

        
        vbox.addWidget(top,1)
        vbox.addWidget(main,5)
        vbox.addWidget(bottom,1)
        
        self.setLayout(vbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        
        self.setWindowTitle('QSplitter demo')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

        if e.key() == QtCore.Qt.Key_A:
            self.star_label[0].setPixmap(self.donut_pixmap)
app = QApplication(sys.argv)
ex =Window()

ex.showFullScreen()
sys.exit(app.exec_())