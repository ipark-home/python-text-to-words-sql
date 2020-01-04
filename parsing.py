import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(url):
    soup = BeautifulSoup(get_html(url), 'lxml')
    pages = soup.find(
        'ul', class_='post-list archive').find_all('a')
    nomers = []
    for page in pages:
        nomers.append(page.get('href').split('/')[1])
        # nomers.append(page.get('a'))
    return nomers


def replace_td(td):
    return td.replace('\n', '').replace(
        '<td>', '').replace('</td>', '\t').replace('<br/>', '\t')


def get_total_data(url):
    soup = BeautifulSoup(get_html(url), 'lxml')

    ads = soup.find('div', id='post-wrapper').find('div',
                                                   class_='post').find_all('tbody')
    for ad in ads:
        td = ad.find_all('tr')[0].find_all('td')
        # print(td)
        print('=1='+td[0].find('a').string)
        # print('=2='+str(td[2]))
        # print('=2='+str(td[1].find('table', id='int')))
        # .find_all('tr')[0].find_all('td')
        tdd2 = str(td[2].find('table', id='int').find('td')).split('<br/>')
        tdd3 = replace_td(str(td[3]))
        tdd4 = replace_td(str(td[4]))
        tdd5 = td[5].find('b').string

        # print('=3='+str(tdd2))
        print('=4='+str(tdd3))
        print('=5='+str(tdd4))
        print('=6='+str(tdd5))
        # i = 0
        # for atd in tdd4:
        #     print(str(i)+':'+str(atd))
        #     i += 1


def getWordAtr(html):
    soup = BeautifulSoup(get_html(url), 'lxml')
    pages = soup.find(
        'ul', class_='post-list archive').find_all('a')
    nomers = []
    for page in pages:
        nomers.append(page.get('href').split('/')[1])
        # nomers.append(page.get('a'))
    return nomers

    # print(ads)


def getWordCambridge(word):
    url = "https://dictionary.cambridge.org/search/english-russian/direct/?q="+word
    import urllib
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
    try:
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

def main():
    arr = getWord('prepare')
        if not arr None
        for el in arr:
            print(el)
    # for page in pages:
    #     print(url+page)
    # print(page)

    # get_total_data('http://alu.kiev.ua/cat6/')


if __name__ == '__main__':
    main()
