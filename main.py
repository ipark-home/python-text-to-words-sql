# import requests
# import re
# import html.parser as htmlparser

# import os

# parser = htmlparser.HTMLParser()


def load():
    lang =2  # 1 -eng 2 uk
    from FileWords import FileWords
    fw = FileWords('speach20052019.txt')
    fw.readFile()
    fw.getWordsPrint()

    text = 'Speach President ZE 20/05/2019'

    from SqliteWord import SqliteWord
    sw = SqliteWord()
    idText = sw.appendText(text)
    # print(idText)
    cn = len(fw.words)
    i = 0
    # sw.appendLinkWordText((1, fw.words[0], ), idText)
    for word in fw.words:
        print(str(cn)+':'+str(i)+' '+word)
        sw.appendLinkWordText((lang, word, ), idText)
        i += 1


def translate():
    text = 'Overview of Amazon Web Services'
    from SqliteWord import SqliteWord
    sw = SqliteWord()
    idText = sw.appendText(text)
    sw.appendTraslate(idText)


def readTranslate():
    text = 'Overview of Amazon Web Services'
    from SqliteWord import SqliteWord
    sw = SqliteWord()
    idText = sw.appendText(text)
    sw.readTranslate(idText=idText)


def main():
    load()
    #text = 'Speach Persedent ZE 20/05/2019'
    #from SqliteWord import SqliteWord
    #sw = SqliteWord()
    #idText = sw.appendText(text)
    #sw.appendSentenceFromWords(idText=idText)


if __name__ == '__main__':
    main()

