import re
import urllib.request
import bs4 as bs

url = 'https://gamerant.com/ps5-game-release-dates/'

page = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(page, 'lxml')
ul_tags = soup.find_all('ul')
li_tags = []
for ul_tag in ul_tags:
    for li_tag in ul_tag.find_all('li'):
        if re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}',
                     li_tag.get_text()):
            li_tags.append(li_tag.text.strip())
print(li_tags)
