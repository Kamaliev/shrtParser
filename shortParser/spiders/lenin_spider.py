from pathlib import Path
from bs4 import BeautifulSoup
import scrapy


class LeninSpider(scrapy.Spider):
    name = "lenin"
    domain = 'https://cyberleninka.ru'

    def start_requests(self):
        urls = [
            self.domain
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.body.decode('utf-8'), 'lxml')

        ul = soup.findAll('ul', {'class': 'oecd'})
        for li in ul:
            for i in li.findAll('a'):
                yield scrapy.Request(url=self.domain + i['href'], callback=self.parse_category)

    def parse_category(self, response, **kwargs):
        soup = BeautifulSoup(response.body.decode('utf-8'), 'lxml')
        main = soup.findAll('div', {'class': 'full'})
        for div in main:
            for article in div.findAll('a'):
                yield scrapy.Request(url=self.domain + article['href'], callback=self.parse_article)

        paginator = soup.find('ul', {'class': 'paginator'})
        active = int(paginator.find('span', {'class': 'active'}).get_text())

        max_url = paginator.find('a', {'class': 'icon'})['href']
        max_pag = int(max_url.split('/')[-1])
        if active < max_pag:
            yield scrapy.Request(url=self.domain + max_url[:max_url.rfind('/') + 1] + str(active + 1),
                                 callback=self.parse_category)

    def parse_article(self, response, **kwargs):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        Path(filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')

        soup = BeautifulSoup(response.body.decode('utf-8'), 'lxml')

        annotation = soup.find('div', {'class': 'full abstract'})

        if annotation:
            desc = annotation.find('p').get_text()
            pdf = soup.find('meta', {'name': 'citation_pdf_url'})['content']
            yield {'desc': desc, 'pdf': pdf, 'url': response.url}
