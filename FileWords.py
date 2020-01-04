
class FileWords():
    def __init__(self, nameFile):
        self.nameFile = nameFile
        self.countWords = 0
        self.words = []

    def split_line(self, text):
        words = text.split()
        for word in words:
            for ch in ['“', '”', '.', ',', '?', '"', '*', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', ']', '-', ':', '!', '(', ')', ';']:
                if ch in word:
                    word = word.replace(ch, '')
            for wr in ['I']:
                if not wr in word:
                    word = word.lower()
            word = word.strip(' \t\n\r')
            if (len(word) > 1 and len(word) < 32) or 'I' in word:
                #  self.countWords += 1
                self.words.append(word)
                # linkTextWordAppend('The_Old_Man_and_the_Sea', word, 1)
                # wordAppend(word, 2)

    def getWordsPrint(self):
        for word in self.words:
            print(word)

    def readFile(self):
        # self.countWords
        # self.countWords = 0
        with open(self.nameFile, 'rb') as fh:
            while True:
                line = fh.readline().decode("UTF-8")
                # print(line)
                self.split_line(line)
                if not line:
                    break
        fh.close()

    def __del__(self):
        pass
