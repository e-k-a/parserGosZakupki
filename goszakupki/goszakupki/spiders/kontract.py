import scrapy

class CatalogSpider(scrapy.Spider):
    name = 'kontract'
    allowed_domains = ['zakupki.gov.ru']
    start_urls = ['https://zakupki.gov.ru/']
    pages_count = 100

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://zakupki.gov.ru/epz/contract/search/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&savedSearchSettingsIdHidden=&fz44=on&contractStageList_0=on&contractStageList_1=on&contractStageList_2=on&contractStageList_3=on&contractStageList=0%2C1%2C2%2C3&contractInputNameDefenseOrderNumber=&contractInputNameContractNumber=&contractPriceFrom=&rightPriceRurFrom=&contractPriceTo=&rightPriceRurTo=&priceToUnitGWS=&contractCurrencyID=-1&nonBudgetCodesList=&budgetLevelsIdHidden=&budgetLevelsIdNameHidden=%7B%7D&budgetName=&customerPlace=&customerPlaceCodes=&contractDateFrom=&contractDateTo=&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&placingWayList=&selectedLaws=&sortBy=UPDATE_DATE&pageNumber={page}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.registry-entry__header-mid__number ::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        GenInf = {}
        for GI in response.xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div/section'):
            Value = GI.xpath('span[2]/text()').extract_first('').strip()
            if Value:
                GenInf[GI.xpath('span[1]/text()').extract_first('').strip() ] =  GI.xpath('span[2]/text()').extract_first('').strip()
            else:
                GenInf[GI.xpath('span[1]/text()').extract_first('').strip() ] =  GI.xpath('span/a/text()').extract_first('').strip()
        ChangeKontr = {}
        for CK in response.xpath('/html/body/div[2]/div/div[2]/div[2]/div/div/div/section'):
            ChangeKontr[CK.xpath('span[1]/text()').extract_first('').strip() ] =  CK.xpath('span[2]/text()').extract_first('').strip()     
        CustInf = {}
        for CI in response.xpath('/html/body/div[2]/div/div[2]/div[3]/div/div/div/section'):
            Value = CI.xpath('span[2]/text()').extract_first('').strip()
            if Value:
                CustInf[CI.xpath('span[1]/text()').extract_first('').strip() ] =  CI.xpath('span[2]/text()').extract_first('').strip()
            else:
                CustInf[CI.xpath('span[1]/text()').extract_first('').strip() ] =  CI.xpath('span/a/text()').extract_first('').strip() 
        GenData = {}
        for GD in response.xpath('/html/body/div[2]/div/div[2]/div[3]/div/div/div/section'):
            GenData[GD.xpath('span[1]/text()').extract_first('').strip() ] =  GD.xpath('span[2]/text()').extract_first('').strip()   


        #urlTable = 'https://zakupki.gov.ru' + response.xpath('/html/body/div[2]/div/div[1]/div[3]/div/a[2]/@href').extract_first()
        #urlHelp = response.urljoin(response.xpath('/html/body/div[2]/div/div[1]/div[3]/div/a[2]/@href').extract_first())
        
        

        item = {
            'номер' : response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/span[1]/a//text()").extract_first('').strip(),
            'url': response.request.url,
            'статус контракта' : response.css('.cardMainInfo__state ::text').extract_first('').strip(),
            'объект закупки' : response.xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/span/text()').extract_first("").strip(),
            'заказчик' : response.xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/div/section[1]/span[2]/a/text()").extract_first(' ').strip(),
            'начальная цена' : response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[1]/span[2]/text()").extract_first(' ').strip(),
            'Заключение контракта' : response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/span[2]/text()").extract_first(' ').strip(),
            'Срок исполнения' : response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/span[2]/text()").extract_first(' ').strip(),
            'Размещен контракт в реестре контрактов' : response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/span[2]/text()").extract_first(' ').strip(),
            'Обновлен контракт в реестре контрактов' : response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[4]/span[2]/text()").extract_first(' ').strip(),
            'Общая информация' : GenInf,
            'Информация о заказчике' : CustInf,
            'Общие данные' : GenData,


        }

        
        
        yield item

