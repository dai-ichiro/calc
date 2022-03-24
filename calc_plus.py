
import random
import datetime
import vlc

from PyQt6.QtCore import Qt, QTime, QTimer, QEventLoop
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QKeySequence

from constructGUI import construct

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
        self.star_image = QPixmap('./sound/star.png')
        self.num_image = [QPixmap('./sound/%d.png'%i) for i in range(10)]
        self.plus_image = QPixmap('./sound/plus.png')
        self.question = True
        self.q1 = 0
        self.q2 = 0
        self.real_answer = 0
        self.num_button_ready = False
        self.start_button_ready = True
        self.ok_count = 0
        self.time1 = None
        
    def initUI(self):


        ### header ###
        top = QFrame()
        header_layout = QHBoxLayout()
        self.star_label = [construct(QLabel(), 'settings.yaml', 'star_label') for i in range(10)]
        for i in range(10):
            header_layout.addWidget(self.star_label[i])
        top.setLayout(header_layout)
        ### header ###

        ### main ###
        main = QFrame()
        main.setLineWidth(2)
        main.setFrameStyle(QFrame.Shape.Box.value | QFrame.Shadow.Plain.value)
        main_layout = QHBoxLayout()
        main_ratio = [2,1,2]
        self.num_label = [QLabel() for i in range(3)]
        for i in range(3):
            main_layout.addWidget(self.num_label[i], main_ratio[i])
        main.setLayout(main_layout)
        ### main ###

        ### footer ###
        self.timer_label = construct(QLabel(), 'settings.yaml', 'timer_label')
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
        if e.key() == Qt.Key.Key_Escape:
            self.close()

        ### game start ###
        if e.key() == Qt.Key.Key_Return and self.start_button_ready == True:
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
            loop.exec()
            
            self.startTimer()
            self.make_question()

        if QKeySequence(e.key()).toString() == str(self.real_answer) and self.num_button_ready == True:
            self.correct_answer()

    def make_question(self):
        self.q1 = random.randint(1, q1_max_num)
        self.q2 = random.randint(1, q2_max_num)
        self.real_answer = self.q1 + self.q2

        ### display ###
        self.set_image_into_label(self.num_image[self.q1], self.num_label[0])
        self.set_image_into_label(self.plus_image, self.num_label[1])
        self.set_image_into_label(self.num_image[self.q2], self.num_label[2])

        self.num_button_ready = True

    def correct_answer(self):
        self.num_button_ready = False
        self.ok_count += 1
        
        self.set_image_into_label(self.star_image, self.star_label[self.ok_count -1])
        if self.ok_count == 10:
            self.now_playing = False
            self.stopTimer()
            player2.play()
            loop = QEventLoop()
            QTimer.singleShot(4000, loop.quit)
            loop.exec()
            self.start_button_ready = True
        else:
            player1.play()
            loop = QEventLoop()
            QTimer.singleShot(800, loop.quit)
            loop.exec()
            for i in range(3):
                self.num_label[i].clear()
            loop = QEventLoop()
            QTimer.singleShot(200, loop.quit)
            loop.exec()
            self.make_question()
    
    def set_image_into_label(self, image, label):
        w = label.width()
        h = label.height()
        label.setPixmap(image.scaled(w-4, h-4, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    
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

if __name__ == "__main__":
    app = QApplication([])
    ex =Window()
    ex.showFullScreen()
    app.exec()
