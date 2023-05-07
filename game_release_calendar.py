import re

import urllib.request
import bs4 as bs


class Scaper:
    def __init__(self, site):
        """Create an instance for scaper class."""
        self.site = site
        self.li_tags = []

    def scaper(self):
        """Scraps data from site."""
        url = self.site
        page = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(page, 'lxml')
        ul_tags = soup.find_all('ul')
        self.li_tags = [li_tag.text.strip() for ul_tag in ul_tags for li_tag in ul_tag.find_all('li') if
                        re.match(
                            r'^(January|February|March|April|May|June|July|August|September|October|November|December)',
                            li_tag.get_text().strip())]


ps5 = Scaper('https://gamerant.com/ps5-game-release-dates/')
ps5.scaper()
