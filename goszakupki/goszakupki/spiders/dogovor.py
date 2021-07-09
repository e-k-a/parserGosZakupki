import scrapy

class CatalogSpider(scrapy.Spider):
    name = 'dogovor'
    start_urls = ['https://zakupki.gov.ru/']
    pages_count = 5

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://zakupki.gov.ru/epz/contractfz223/search/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&savedSearchSettingsIdHidden=&statuses_0=on&statuses_1=on&statuses_2=on&statuses_3=on&statuses=0%2C1%2C2%2C3&priceFrom=&priceTo=&currencyId=-1&contract223DateFrom=&contract223DateTo=&publishDateFrom=&publishDateTo=&sortBy=BY_UPDATE_DATE&pageNumber={page}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.registry-entry__header-mid__number ::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = {
            'номер' : response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/text()").extract_first().strip(),
            'url': response.request.url,
            #'заказчик' : response.xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/div/section[1]/span[2]/a/text()").extract_first(' ').strip(),
            #'Общие данные' : GenData,



        }

        
        
        yield item
