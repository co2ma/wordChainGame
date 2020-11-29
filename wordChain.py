import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from names import *


class WordChain(QWidget):
    def __init__(self):
        super().__init__()
        self.startStop = True
        self.setWindowTitle('wordChainGame')
        self.setWindowIcon(QIcon("icon.png"))
        #변수 선언
        self.lastWord = '' # 마지막 한 글자 저장용
        self.wordStack = [] # 단어 중복 확인용
        self.curruntTurn = 1 #현재 차례

        #요소 선언
        self.mainLayout = QVBoxLayout()
        self.statusLine = QHBoxLayout()
        self.gameWindow = QTextEdit(); self.gameWindow.setReadOnly(True); self.gameWindow.setFontPointSize(12); self.gameWindow.setText(COLOR_BLUE + "#끝말잇기 게임");
        self.settingGame = QHBoxLayout()
        self.dueumRule = QCheckBox()
        self.oneKillWord = QCheckBox()
        self.difficultyBox = QComboBox(); self.difficultyBox.addItems(difficultyName)
        self.newGameStartButton = QPushButton("게임 시작"); self.newGameStartButton.clicked.connect(self.startButton)
        self.writeAnswer = QLineEdit(); self.writeAnswer.returnPressed.connect(self.returnEnterEvent)
        self.frontText = QLabel(TEXTSIZE + str(self.curruntTurn))
        self.backText = QLabel(TEXTSIZE + f" / {displayDiff[self.difficultyBox.currentText()]}"+ " 턴")

        #MainLayout에 추가
        self.statusLine.addStretch(1)
        self.statusLine.addWidget(self.frontText)
        self.statusLine.addWidget(self.backText)
        self.mainLayout.addLayout(self.statusLine)
        self.mainLayout.addWidget(self.gameWindow)
        self.settingGame.addStretch(1)
        self.settingGame.addWidget(self.dueumRule)
        self.settingGame.addWidget(QLabel("두음 법칙 허용"))
        self.settingGame.addWidget(self.oneKillWord)
        self.settingGame.addWidget(QLabel("추가 예정"))
        self.settingGame.addWidget(self.difficultyBox)
        self.settingGame.addWidget(self.newGameStartButton)
        self.mainLayout.addLayout(self.settingGame)
        self.mainLayout.addWidget(self.writeAnswer)


        self.setLayout(self.mainLayout)

    def returnEnterEvent(self): # 엔터를 눌렀을때 반응
        pass

    def startButton(self): # 시작 버튼을 눌렀을때 반응
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = WordChain()
    game.show()
    sys.exit(app.exec_())

# 추가 해야할 기능 승리 조건 , 턴 기능 , 두음법칙 기능 , 추가 기능들
