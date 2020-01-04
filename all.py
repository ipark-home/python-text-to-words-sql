import os
import sqlite3
import requests
import re
# import winsound
import html.parser as htmlparser

parser = htmlparser.HTMLParser()

url = "https://translate.google.com/translate_tts"
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"}


# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
DB_NAME = 'F:\SQLite\words\words.db'
# FILE_NAME = 'msThe_Old_Man_and_the_Sea.txt'
FILE_NAME = 'kotlarevski2.txt'


def split_line(text):
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
            global countWords
            countWords += 1
            print(str(countWords)+' '+word)
            linkTextWordAppend('The_Old_Man_and_the_Sea', word, 1)
            # wordAppend(word, 2)


def split_line_Append(textline, idtext, idtypeword):
    words = textline.split()
    for word in words:
        for ch in ['“', '”', '.', ',', '?', '"', '*', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', ']', '-', ':', '!', '(', ')', ';']:
            if ch in word:
                word = word.replace(ch, '')
        for wr in ['I']:
            if not wr in word:
                word = word.lower()
        word = word.strip(' \t\n\r')
        if (len(word) > 1 and len(word) < 32) or 'I' in word:
            global countWords
            countWords += 1
            print(str(countWords)+' '+word)
            # linkTextWordAppend('The_Old_Man_and_the_Sea', word, 1)
            linkIdTextWordAppend(idtext, word, idtypeword)
            # wordAppend(word, 2)


def readFileAppend():
    global countWords
    countWords = 0
    idtypeword = 2
    idtext = textAppend('Енеїда')
    # file handle fh
    # fh = open(FILE_NAME)
    with open(FILE_NAME, 'rb') as fh:
        while True:
            # read line
            line = fh.readline().decode("UTF-8")
            split_line_Append(line, idtext, idtypeword)
            # check if line is not empty
            if not line:
                break
    fh.close()


def readFile():
    global countWords
    countWords = 0
    # file handle fh
    # fh = open(FILE_NAME)
    with open(FILE_NAME, 'rb') as fh:
        while True:
            # read line
            line = fh.readline().decode("UTF-8")
            # in python 2, print line
            # in python 3
            split_line(line)
            # check if line is not empty
            if not line:
                break
    fh.close()

# Imports the Google Cloud client library


def translate(text):
    # Instantiates a client
    from google.cloud import translate
    translate_client = translate.Client()

    # The text to translate
    # text = u'Hello, world!'
    # The target language
    target = 'uk'
    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)
    # print(u'Text: {}'.format(text))
    # print(u'Translation: {}'.format(translation['translatedText']))
    return translation['translatedText']


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def textSearch(text):
    arr = (text,)
    cur = conn.cursor()
    cur.execute('SELECT _id FROM texts WHERE name=?', arr)
    try:
        res = cur.fetchone()[0]
    except:
        res = -1
    return res


def textAppend(text):
    res = textSearch(text)
    if res == -1:
        cur = conn.cursor()
        cur.execute('INSERT INTO texts(name,id_type) VALUES (?,?)', (text, 1,))
        res = cur.lastrowid
        conn.commit()
    print('id:'+str(res)+' text:'+text)
    return res


def wordSearch(word, idtype=1):
    arr = (word, idtype,)
    cur = conn.cursor()
    cur.execute('SELECT _id FROM words WHERE name=? and id_type=?', arr)
    try:
        res = cur.fetchone()[0]
    except:
        res = -1
    return res


def wordAppend(word, idtype):
    res = wordSearch(word, idtype)
    if res == -1:
        cur = conn.cursor()
        cur.execute('INSERT INTO words(name,id_type) VALUES (?,?)',
                    (word, idtype,))
        res = cur.lastrowid
        conn.commit()
    return res


def linkWordsAppend(parentWord, childWord, typeLink=1):
    idParentWord = wordAppend(parentWord, 1)
    idChildWord = wordAppend(childWord, 2)
    arr = (idParentWord, idChildWord, typeLink,)
    cur = conn.cursor()
    cur.execute(
        'select * from wordlinks WHERE id_parent=? and id_child=? and id_type=?', arr)
    try:
        res = cur.fetchone()[0]
    except:
        cur.execute(
            'INSERT INTO wordlinks(id_parent,id_child,id_type) VALUES (?,?,?)', arr)
        res = cur.lastrowid
        conn.commit()
    # return res


def wordAllRead(idtype=1):
    arr = (idtype,)
    cur = conn.cursor()
    try:
        for row in cur.execute('SELECT _id,name FROM words WHERE id_type=? ', arr):
            word = row[1]
            trans = translate(word)
            linkWordsAppend(word, trans, 1)
            print(word+':'+trans)
        res = 1
    except:
        res = -1
    return res


def linkTextWordAppend(text, typeword):
    idtext = textAppend(text)
    linkIdTextWordAppend(idtext, word, typeword)


def linkIdTextWordAppend(idtext, word, typeword):
    idword = wordAppend(word, typeword)
    arr = (idtext, idword, )
    cur = conn.cursor()
    cur.execute(
        'select * from textwordlinks WHERE id_text=? and id_word=? ', arr)
    try:
        res = cur.fetchone()[0]
        cur = conn.cursor()
        cur.execute(
            'UPDATE textwordlinks set counts=counts+1 WHERE id_text=? and id_word=? ', arr)
    except:
        cur.execute(
            'INSERT INTO textwordlinks(id_text,id_word) VALUES (?,?)', arr)
        res = cur.lastrowid
        conn.commit()
    # return res


def fileNameMP3(text, p_tl='en'):
    return './mp3/'+p_tl+'/'+text.replace(" ", "")+'.mp3'


def saveFileSpeechGoogle(text, p_tl='en'):
    if p_tl == 'uk':
        filename = fileNameMP3(transliterate(text), p_tl)
    else:
        filename = fileNameMP3(text, p_tl)

    params = {
        'client': 'tw-ob',
        'ie':     'UTF-8',
        'tl':     p_tl,
        'q':      text
    }
    r = requests.get(url, params=params, headers=headers)
    with open(filename, 'wb') as f:
        f.write(r.content)

    f.close()
    r.close()


def transliterate(string):
    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'H',
                       u'Ґ': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'З': u'Z',
                       u'И': u'Y',
                       u'І': u'I',
                       u'Ї': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Ь': u'',
                       u"'": u"", }

    capital_letters_transliterated_to_multiple_letters = {u'Є': u'Ie',
                                                          u'Ж': u'Zh',
                                                          u'Х': u'Kh',
                                                          u'Ц': u'Ts',
                                                          u'Ч': u'Ch',
                                                          u'Ш': u'Sh',
                                                          u'Щ': u'Shch',
                                                          u'Ю': u'Iu',
                                                          u'Я': u'Ia', }

    capital_letters_in_first_position = {u'Є': u'Ye',
                                         u'Ї': u'Yi',
                                         u'Й': u'Y',
                                         u'Ю': u'Yu',
                                         u'Я': u'Ya', }

    lower_case_letters = {u'а': u'a',
                          u'б': u'b',
                          u'в': u'v',
                          u'г': u'h',
                          u'ґ': u'g',
                          u'д': u'd',
                          u'е': u'e',
                          u'є': u'ie',
                          u'ж': u'zh',
                          u'з': u'z',
                          u'и': u'y',
                          u'і': u'i',
                          u'ї': u'i',
                          u'й': u'i',
                          u'к': u'k',
                          u'л': u'l',
                          u'м': u'm',
                          u'н': u'n',
                          u'о': u'o',
                          u'п': u'p',
                          u'р': u'r',
                          u'с': u's',
                          u'т': u't',
                          u'у': u'u',
                          u'ф': u'f',
                          u'х': u'kh',
                          u'ц': u'ts',
                          u'ч': u'ch',
                          u'ш': u'sh',
                          u'щ': u'shch',
                          u'ь': u'',
                          u"'": u"",
                          u'ю': u'iu',
                          u'я': u'ia', }

    lower_case_letters_in_first_position = {u'є': u'ye',
                                            u'ї': u'yi',
                                            u'й': u'y',
                                            u'ю': u'yu',
                                            u'я': u'ya', }

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.items():
        string = re.sub(
            r'{0:s}([а-я])'.format(cyrillic_string), r'%s\1' % latin_string, string)

    for dictionary in (capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in dictionary.items():
            string = string.replace(cyrillic_string, latin_string)

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.items():
        string = string.replace(cyrillic_string, latin_string.upper())

    return string


def readTextWordSQLite():
    arr = (1, )
    cur = conn.cursor()
    cur.execute('SELECT f._id, f.name fname, a.name lname, t.counts  FROM words F, wordlinks l, words a, textwordlinks t  where f.id_type=? and l.id_parent=f._id and l.id_child=a._id and f._id=t.id_word and t.id_text=2 order by t.counts desc', arr)
    rows = cur.fetchall()
    with open('ukwords.txt', 'x', encoding="utf-8") as fh:
        for row in rows:
            if row[2] != '':
                uktext = parser.unescape(row[2]).replace("-", " ")
                # uktext = row[2]
                # txt = row[1]+';'+uktext+';' + \
                #     row[1].replace(
                #         "-", "").replace(" ", "")+'.mp3;' + \
                #     transliterate(uktext).replace(
                #         "-", "").replace(" ", "")+'.mp3;\n'
                txt = row[1]+'\t'+uktext+'\t\t\t\n'
                print(txt)
                fh.write(txt)
                # saveFileSpeechGoogle(uktext, p_tl='uk')
                # saveFileSpeechGoogle(row[1])
        # try:
    #     res = cur.fetchall()
    # # except:
    fh.close()
    cur.close()

# def conn:
# conn = sqlite3.connect('F:\SQLite\words\words.db')


# c.execute('SELECT * FROM comments')
# for row in c.execute('SELECT * FROM comments'):
#     print(row)
# print c.fetchone()

# cursor.execute('SELECT * FROM comments')
# result = cursor.fetchall()

# print(result)

# conn = db_connect(DB_NAME)
# cursor = conn.cursor()

# s = wordSearch('Hi')
# print(s)

# idtext = textAppend('Incorrect number of bindings supplied.')
# linkTextWordAppend('Incorrect number of bindings supplied.', 'number', 1)
# print("Hi")
# conn.close()


#
conn = db_connect(DB_NAME)
# readFile()
# readFileAppend()
readTextWordSQLite()
# print(transliterate('пархоменко'))

# linkTextWordAppend(text, word, 2);


# trans = translate('one')
# print(wordAllRead(1))
# print(word)
# trans = translate(word)
# print(trans)
