import os

def wordCreate():
    os.mkdir("wordAll")
    with open("wordDAT/wordSet.txt",'r') as f:
        with open("wordDAT/wordList.txt", 'r') as f2:
            setList = f.readlines()
            word = f2.readlines()
            for i in setList:
                i = i.replace("\n","")
                for j in i:
                    with open(f"wordAll/{j}.txt",'w') as mkfile:
                        pass
            for j in word:
                if j[0] == '?':
                    continue
                with open(f"wordAll/{j[0]}.txt",'a') as words:
                    words.write(j)
