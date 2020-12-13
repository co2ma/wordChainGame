import sys
import os
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from names import *
from wordFunction import wordCreate


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
        self.gameWindow = QTextEdit(); self.gameWindow.setReadOnly(True); self.gameWindow.setFontPointSize(12); self.gameWindow.setText(COLOR_BLUE + "#끝말잇기 게임"); self.gameWindow.append(COLOR_BLUE + "#첫 실행시 단어 분류 작업을 합니다")
        self.settingGame = QHBoxLayout()
        self.dueumRule = QCheckBox()
        self.verbRule = QCheckBox()
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
        self.settingGame.addWidget(self.verbRule)
        self.settingGame.addWidget(QLabel("동사 금지"))
        self.settingGame.addWidget(self.difficultyBox)
        self.settingGame.addWidget(self.newGameStartButton)
        self.mainLayout.addLayout(self.settingGame)
        self.mainLayout.addWidget(self.writeAnswer)


        self.setLayout(self.mainLayout)

    def returnEnterEvent(self): # 엔터를 눌렀을때 반응
        if(self.startStop == True or self.writeAnswer.text() == ''):
            return

        word = self.writeAnswer.text(); self.writeAnswer.clear()

        dueumWord = ''
        if(self.lastWord in DUEUM.keys() and self.dueumRule.isChecked()):
            dueumWord = DUEUM[self.lastWord]
        if (len(word) < 2):
            self.gameWindow.append(COLOR_BLUE + "#두 글자 이상을 입력하세요")
        elif (self.lastWord != word[0] and dueumWord == ''):
            self.gameWindow.append(COLOR_BLUE + "#끝 말을 이어야 합니다!")
        elif (dueumWord != '' and (dueumWord != word[0] and self.lastWord != word[0])):
            self.gameWindow.append(COLOR_BLUE + "#끝 말을 이어야 합니다!")
        elif(word in self.wordStack):
            self.gameWindow.append(COLOR_BLUE + "#같은 단어가 중복 되었습니다.")
        elif(self.verbRule.isChecked() and word[-1] == '다'):
            self.gameWindow.append(COLOR_BLUE + "#동사 금지 룰***")
        else:
            try:
                with open(f"wordAll/{word[0]}.txt", 'r') as f:
                    check = f.readlines()
                    if(word+'\n' in check):
                        self.gameWindow.append("너 : " + word)
                        self.wordStack.append(word)
                        self.curruntTurn += 1
                        self.frontText.setText(TEXTSIZE + str(self.curruntTurn))
                        if (self.curruntTurn > displayDiff[self.difficultyBox.currentText()]):
                            self.gameWindow.append(COLOR_BLUE + "#당신의 승리 입니다")
                            self.gameEnd()
                        else:
                            self.enemyTurn(word[-1])
                    else:
                        self.gameWindow.append(COLOR_BLUE + "#사전에 없는 단어입니다")
            except FileNotFoundError:
                self.wordStack.append(word)
                self.gameWindow.append(COLOR_BLUE + "#당신의 승리 입니다")
                self.gameEnd()



    def gameEnd(self):
        self.startStop = True
        self.newGameStartButton.setText("게임 시작")
        self.wordStack = []
        self.turnSetting()
        self.writeAnswer.clear()
        self.dueumRule.setEnabled(True)
        self.verbRule.setEnabled(True)
        self.difficultyBox.setEnabled(True)

    def enemyTurn(self, word):
        with open(f"wordAll/{word}.txt", 'r') as file:
            line = random.choice(file.readlines()).replace("\n", "")
            if(not line in self.wordStack):
                if(self.verbRule.isChecked() and line[-1] == '다'):
                    self.enemyTurn(word)
                else:
                    self.lastWord = line[-1]
                    self.gameWindow.append(COLOR_RED + "적 : " + line)
                    self.wordStack.append(line)



    def turnSetting(self):
        self.curruntTurn = 1
        self.frontText.setText(TEXTSIZE + str(self.curruntTurn))
        self.backText.setText(TEXTSIZE + f" / {displayDiff[self.difficultyBox.currentText()]}" + " 턴")

    def startButton(self): # 시작 버튼을 눌렀을때 반응
        if (not os.path.isdir("wordAll")):
            wordCreate()
        if (self.startStop == True):
            self.startStop = False
            self.newGameStartButton.setText("항복 하기")
            self.gameWindow.setText(COLOR_BLUE + "#게임을 시작합니다")
            self.turnSetting()
            self.dueumRule.setEnabled(False)
            self.verbRule.setEnabled(False)
            self.difficultyBox.setEnabled(False)
            self.enemyTurn(startWord[random.randint(0, 13)])
        else:
            self.gameWindow.append(COLOR_BLUE + "#당신은 패배 했습니다")
            self.gameEnd()



if __name__ == "__main__":

    app = QApplication(sys.argv)
    game = WordChain()
    game.show()
    sys.exit(app.exec_())
