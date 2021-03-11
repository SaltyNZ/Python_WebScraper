import requests
from bs4 import BeautifulSoup


'''
catagory = "motels"

#Find the number of pages
def findnumofpages(catagory): #Find the Number of Pages
    page_link = requests.get(f"https://www.nzdirectory.co.nz/{catagory}.html")
    Soup = BeautifulSoup(page_link.text, 'html.parser')
    PageNum = Soup.find_all('div', id="page_cat")
    ListNum = []

    for Pagelist in PageNum:
        PageDetails = Pagelist.find_all('div', class_="pages")
        numofpages = len(PageDetails)
        ListNum = numofpages
    return ListNum

PageNum = findnumofpages(catagory)

print(PageNum)
'''

def URLsGet(page, Home):
    URLs = []
    html_link = requests.get(page)
    BSoup = BeautifulSoup(html_link.text, 'html.parser')
    cata = BSoup.find('div', id='page_cat')
    if cata is None:
        return []
    links = cata.findChildren('a')
    for link in links:
        URLs.append(Home + link.get('href'))
    return URLs

def URLFinder(CataPage, Home):
    urls_all = []
    html_link = requests.get(CataPage)
    BSoup = BeautifulSoup(html_link.text, 'html.parser')
    table = BSoup.find('table', id='categories')
    links = table.findChildren('a')
    urls_main = []
    for link in links:
        urls_main.append(Home + link.get('href'))
    urls_main.append(CataPage)
    for url in urls_main:
        urls_all.extend(URLsGet(url, Home))
    urls_all.extend(urls_main)
    return urls_all

def scrapepage(url):
    DataSearch = []
    html_link = requests.get(url)
    BSoup = BeautifulSoup(html_link.text, 'html.parser')
    DirList = BSoup.find(id='directory_listings')
    DirList_lis = DirList.findChildren('li')

    for li in DirList_lis:
        if li.find('div', class_='listing_content') is not None:
            business = li.find('a').get_text()
            content = li.find('p', class_='address')
            if content is None:
                continue
            content = content.get_text()
            if content.find('+') == -1:
                continue
            address, phonenum = content.split('+', 1)
            for word in business.split(' '):
                address = address.replace(word, '')
            address = address.lstrip(', ')
            phonenum = '+' + phonenum
            DataSearch.append({'Business': business, 'Address': address, 'Phone Number': phonenum})
        return DataSearch
            
def getList(CataPage, Home):
    data = []
    webpages = URLFinder(CataPage, Home)
    for page in webpages:
        data.extend(scrapepage(page))
    print(len(data))
    print(data)
    return data

getList('https://www.nzdirectory.co.nz/electronics.html', 'https://www.nzdirectory.co.nz/')
