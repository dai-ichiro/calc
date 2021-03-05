
import random
import datetime
import vlc

import sys
from PyQt5.QtCore import Qt, QTime, QTimer, QEventLoop
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QKeySequence

############################################
q1_max_num = 4
q2_max_num = 4
############################################

player0 = vlc.MediaListPlayer()
player1 = vlc.MediaListPlayer()
player2 = vlc.MediaListPlayer()

mediaList0 = vlc.MediaList(['./sound/dummy.wav'])
mediaList1 = vlc.MediaList(['./sound/ok.wav'])
mediaList2 = vlc.MediaList(['./sound/ok.wav', './sound/yattane.wav'])

player0.set_media_list(mediaList0)
player1.set_media_list(mediaList1)
player2.set_media_list(mediaList2)

#player0.play()

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.question = True
        self.q1 = 0
        self.q2 = 0
        self.real_answer = 0
        self.num_button_ready = False
        self.start_button_ready = True
        self.ok_count = 0
        self.time1 = None
        
    def initUI(self):
        
        self.donut_pixmap = QPixmap('./sound/star.png')
        self.num_pixmap = [QPixmap('./sound/%d.png'%i) for i in range(10)]
        self.plus_pixmap = QPixmap('./sound/plus.png')
        ### header ###
        top = QFrame()
        top.setFrameShape(QFrame.StyledPanel)
        header_layout = QHBoxLayout()
        self.star_label = [QLabel() for i in range(10)]
        for i in range(10):
            self.star_label[i].setFrameStyle(QFrame.Box | QFrame.Plain)
            self.star_label[i].setAlignment(Qt.AlignCenter)
            header_layout.addWidget(self.star_label[i])
        top.setLayout(header_layout)
        ### header ###

        ### main ###
        main = QFrame()
        main.setFrameStyle(QFrame.Box | QFrame.Plain)
        main_layout = QHBoxLayout()
        main_ratio = [2,1,2]
        self.num_label = [QLabel() for i in range(3)]
        for i in range(3):
            self.num_label[i].setFrameStyle(QFrame.NoFrame)
            self.num_label[i].setAlignment(Qt.AlignCenter)
            main_layout.addWidget(self.num_label[i], main_ratio[i])
        main.setLayout(main_layout)
        ### body ###

        ### footer ###
        self.timer_label = QLabel()
        self.timer_label.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Times", 36, QFont.Bold))
        ### footer ###

        vbox = QVBoxLayout()
        vbox.addWidget(top,1)
        vbox.addWidget(main,5)
        vbox.addWidget(self.timer_label,1)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        
        self.setLayout(vbox)        

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

        ### game start ###
        if e.key() == Qt.Key_Return and self.start_button_ready == True:
            self.start_button_ready = False
            self.num_button_ready = True
            self.ok_count = 0
            for i in range(10):
                self.star_label[i].clear()
            for i in range(3):
                self.num_label[i].clear()
            self.timer_label.clear()
            
            player0.play()

            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            
            self.startTimer()
            self.make_question()

        if QKeySequence(e.key()).toString() == str(self.real_answer) and self.num_button_ready == True:
            self.correct_answer()

    def make_question(self):
        self.q1 = random.randint(1, q1_max_num)
        self.q2 = random.randint(1, q2_max_num)
        self.real_answer = self.q1 + self.q2

        ### display ###
        self.set_image_into_label(self.num_pixmap[self.q1], self.num_label[0])
        self.set_image_into_label(self.plus_pixmap, self.num_label[1])
        self.set_image_into_label(self.num_pixmap[self.q2], self.num_label[2])

        self.num_button_ready = True

    def correct_answer(self):
        self.num_button_ready = False
        self.ok_count += 1
        self.set_image_into_label(self.donut_pixmap, self.star_label[self.ok_count -1])
        if self.ok_count == 10:
            self.now_playing = False
            self.stopTimer()
            player2.play()
            loop = QEventLoop()
            QTimer.singleShot(4000, loop.quit)
            loop.exec_()
            self.start_button_ready = True
        else:
            player1.play()
            loop = QEventLoop()
            QTimer.singleShot(800, loop.quit)
            loop.exec_()
            for i in range(3):
                self.num_label[i].clear()
            loop = QEventLoop()
            QTimer.singleShot(200, loop.quit)
            loop.exec_()
            self.make_question()
        
    def set_image_into_label(self, image, label):
        w = label.width()
        h = label.height()
        label.setPixmap(image.scaled(w-2, h-2, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def startTimer(self):
        self.time1 = QTime.currentTime()
        delta = datetime.timedelta(0)
        self.timer_label.setText(str(delta))
        self.timer.start(1000)

    def stopTimer(self):
        self.timer.stop()

    def on_timeout(self):
        time2 = QTime(self.time1).secsTo(QTime.currentTime())
        delta = datetime.timedelta(seconds=time2)
        self.timer_label.setText(str(delta))

app = QApplication(sys.argv)
ex =Window()

ex.showFullScreen()
sys.exit(app.exec_())