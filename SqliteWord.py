

class SqliteWord:

    def __init__(self):
        self.DB_NAME = 'F:/SQLite/words/words.db'
        self.conn = None
        self.connect()
        # import sqlite3
        # self.conn = sqlite3.connect(self.DB_NAME)
        # import sqlite3

    def connect(self):
        import sqlite3
        self.conn = sqlite3.connect(self.DB_NAME)
        # self.conn = self.db.db_connect(self.DB_NAME)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def closeConn(self):
        self.conn.close()

    def findWord(self, word, idtype=1):
        if not self.conn:
            self.connect()
        cur = self.cursor()
        cur.execute('SELECT _id FROM words WHERE name=? and id_type=?',
                    (word, idtype,))
        try:
            res = cur.fetchone()[0]
        except:
            res = 0
        return res

    def appendLinkWords(self, parent, child, typeLink=1):
        idParent = appendWord(parent[1], parent[0])
        idChild = appendWord(child[1], child[0])
        arr = (idParentWord, idChildWord, typeLink,)
        cur = self.cursor()
        cur.execute(
            'select * from wordlinks WHERE id_parent=? and id_child=? and id_type=?', arr)
        try:
            res = cur.fetchone()[0]
        except:
            cur.execute(
                'INSERT INTO wordlinks(id_parent,id_child,id_type) VALUES (?,?,?)', arr)
            res = cur.lastrowid
            self.commit()

    def appendWord(self, word, idtype):
        res = self.findWord(word, idtype)
        if not res:
            cur = self.cursor()
            cur.execute('INSERT INTO words(name,id_type) VALUES (?,?)',
                        (word, idtype,))
            res = cur.lastrowid
            self.commit()
        return res

    def appendLinkWordText(self, word, idText):
        idWord = self.appendWord(word[1], word[0])
        # print(word[1])
        # print(idWord)
        # # return 1
        arr = (idText, idWord, )
        cur = self.cursor()
        cur.execute(
            'select * from textwordlinks WHERE id_text=? and id_word=? ', arr)
        try:
            res = cur.fetchone()[0]
            cur.execute(
                'UPDATE textwordlinks set counts=counts+1 WHERE id_text=? and id_word=? ', arr)
        except:
            cur.execute(
                'INSERT INTO textwordlinks(id_text,id_word) VALUES (?,?)', arr)
            res = cur.lastrowid

        self.commit()

    def searchText(self, text):
        # if self.conn is None:
        #     self.connect()
        cur = self.cursor()
        cur.execute('SELECT _id FROM texts WHERE name=?', (text,))
        try:
            res = cur.fetchone()[0]
        except:
            res = 0
        return res

    def appendText(self, text):
        res = self.searchText(text)
        if not res:
            print(text)
            cur = self.cursor()
            cur.execute(
                'INSERT INTO texts(name,id_type) VALUES (?,?)', (text, 1,))
            res = cur.lastrowid
            self.commit()
        self.textId = res
        return res

    def appendLinkWords(self, parentWord, childWord, typeLink=1):
        idParentWord = self.appendWord(parentWord, 1)
        idChildWord = self.appendWord(childWord, 2)
        arr = (idParentWord, idChildWord, typeLink,)
        cur = self.cursor()
        cur.execute(
            'select * from wordlinks WHERE id_parent=? and id_child=? and id_type=?', arr)
        try:
            res = cur.fetchone()[0]
        except:
            cur.execute(
                'INSERT INTO wordlinks(id_parent,id_child,id_type) VALUES (?,?,?)', arr)
            res = cur.lastrowid
            self.commit()

    def appendTraslate(self, idText=4):
        arr = (idText, )
        cur = self.cursor()
        from TranslateUK import TranslateUK
        for row in cur.execute('''
                    select w._id, w.name FROM textwordlinks l, words w
                        where w._id=l.id_word
                          and l.id_text=?
                          and not exists(select null from wordlinks wl
                                         where wl.id_type=1 and wl.id_parent=w._id)
                    ''', (idText, )):
            word = row[1]
            print(word)
            tr = TranslateUK()
            transUK = tr.get(word)
            print(transUK)
            self.appendLinkWords(
                parentWord=word, childWord=transUK, typeLink=1)
            # linkWordsAppend(word, trans, 1)
            # print(word+':'+trans)

    def readTranslate(self, idText=4):
        arr = (idText, )
        cur = self.cursor()
        i = 0
        with open('engukwords.txt', 'w', encoding="utf-8") as fh:
            for row in cur.execute('''
                        select
                            w.name eng,t.name ukr,l.counts
                        FROM textwordlinks l,words w,wordlinks wl,words t
                        where w._id=l.id_word
                        and l.id_text=?
                        and wl.id_type=1 and wl.id_parent=w._id
                        and wl.id_child=t._id
                        order by l.counts desc
                    ''', (idText, )):
                i += 1
                line = '{:>4} {:<25} {:<30} {:>4} \n'.format(
                    i, row[0], row[1], row[2])
                print(line)
                fh.write(line)

    def getWordCambridge1(self, word):
        url = "https://dictionary.cambridge.org/search/english/direct/?q="+word
        import urllib
        import requests
        from bs4 import BeautifulSoup
        # from urllib import urllib
        try:
            r = urllib.request.urlopen(url)
            # print(r)
            soup = BeautifulSoup(r, "lxml")
            # print(soup)
            # soup = BeautifulSoup(html, 'lxml')
            # print(soup)
            # content = soup.find('div', class_='entrybox english-russian entry-body')
            # content = soup.find('div', class_='tabs__content mod-more on')
            # content = soup.find(
            #     'div', class_="di $ entry-body__el entry-body__el--smalltop clrd js-share-holder").find('div', class_='h3 di-title cdo-section-title-hw')

            contentAll = soup.find(
                'div', class_="di $ entry-body__el entry-body__el--smalltop clrd js-share-holder")
            contentsMake = contentAll.find(
                'p', class_='def-head semi-flush').find_all('a')
            arr = []
            for content in contentsMake:
                arr.append(content.string)
            # print(arr)
            contentSent = contentAll.find(
                'span', class_='def-body').find_all('span', class_='eg')
            # print(contentSent)
            arr = []
            for content in contentSent:
                arr.append(content.text)
            # print(arr)
            return arr
        except:
            return None

    def getWordCambridge(self, word):
        url = "https://dictionary.cambridge.org/dictionary/english/"+word
        import urllib
        import requests
        from bs4 import BeautifulSoup
        try:
            r = urllib.request.urlopen(url)
            # print(r)
            soup = BeautifulSoup(r, "lxml")
            contentAll = soup.find(
                'div', class_="entry-body__el clrd js-share-holder").find('div', class_='pos-body').find_all('div', class_='sense-block')
            # print(contentAll)
            for content in contentAll:
                cnts = content.find_all('span', class_='eg')
                arr = []
                for cntt in cnts:
                    print(cntt.text)
                    arr.append(cntt.text)
            return arr
        except:
            return None

    def searchSentence(self, text):
        # if self.conn is None:
        #     self.connect()
        cur = self.cursor()
        cur.execute('SELECT _id FROM sentences WHERE name=?', (text,))
        try:
            res = cur.fetchone()[0]
        except:
            res = 0
        return res

    def appendSentence(self, text):
        res = self.searchSentence(text)
        if not res:
            # print(text)
            cur = self.cursor()
            cur.execute(
                'INSERT INTO sentences(name,id_type) VALUES (?,?)', (text, 1,))
            res = cur.lastrowid
            self.commit()
        self.textId = res
        return res

    def appendLinkWordSentence(self, idWord, idSentence):
        arr = (1, idSentence, idWord, )
        cur = self.cursor()
        cur.execute(
            'select * from sentencewordlinks WHERE id_type=? and id_sentence=? and id_word=? ', arr)
        try:
            res = cur.fetchone()[0]
        except:
            cur.execute(
                'INSERT INTO sentencewordlinks(id_type,id_sentence,id_word) VALUES (?,?,?)', arr)
            res = cur.lastrowid

        self.commit()

    def appendSentenceFromWords(self, idText=4):
        # sentences = self.getWordCambridge('setup')
        # return None
        arr = (idText, )
        cur = self.cursor()
        i = 0
        for row in cur.execute('''            
                    select 
                        w._id,w.name 
                    FROM textwordlinks l,words w
                    where w._id=l.id_word 
                    and l.id_text=?
                    and not exists (
                    	SELECT null FROM sentencewordlinks sl where sl.id_word=w._id
                    )
                    order by l.counts desc
                    ''', (idText, )):
            i += 1
            print(str(i)+' '+row[1])
            sentences = self.getWordCambridge(row[1])
            if not sentences is None:
                for sentence in sentences:
                    idSentence = self.appendSentence(sentence)
                    self.appendLinkWordSentence(
                        idWord=row[0], idSentence=idSentence)
                    print(sentence)
