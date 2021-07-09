import scrapy

class CatalogSpider(scrapy.Spider):
    name = 'zakupki'
    #allowed_domains = ['zakupki.gov.ru']
    start_urls = ['https://zakupki.gov.ru/']
    pages_count = 5

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber={page}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes='
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.registry-entry__header-mid__number ::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        
        CheckSite1 = response.css('.cardMainInfo__purchaseLink ::text').extract_first('').strip()
        CheckSite2 =  response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/span/text()").extract_first('').strip(),
        if (CheckSite2):
            GenInf = {}
            
            #GenInf[response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[1]/text()').extract_first('').strip() ] =  response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/span/text()').extract_first('').strip()
            for GI in response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr'):
                Value = GI.xpath('/td[1]/text()').extract_first('').strip()
                if Value:
                    GenInf[GI.xpath('td[1]/span/text()').extract_first('').strip() ] =  GI.xpath('td[2]/span/text()').extract_first('').strip()
                
                #else: /html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[10]/td[1]/span/text()
                #    GenInf[GI.xpath('span[1]/text()').extract_first('').strip() ] =  GI.xpath('span/a/text()').extract_first('').strip()
            
            
            item = {}
            item['номер'] = response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/span//text()").extract_first().strip(),
            item['url'] = response.request.url,
            item['заказчик'] = response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[4]/table/tbody/tr[1]/td[2]/text()').extract_first('').strip(),
            item['объект'] = response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[2]/span//text()').extract_first().strip(),
            #'начальная цена' : response.xpath('//*[@id="lot"]/tbody/tr/td[4]/text()').extract_first().strip(),
            #'Размещено' : response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[7]/td[2]/text()").extract_first(' ').strip(),
            #'Обновлено' : response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[8]/td[2]/text()").extract_first(' ').strip(),
            #'Окончание подачи заявок' : response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[6]/table/tbody/tr[3]/td[2]/span/text()").extract_first(' ').strip(),
            #'Общая информация' : GenInf,


            
            number = response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/span//text()").extract_first().strip()
            urlHelp = f'https://zakupki.gov.ru/223/purchase/public/purchase/info/lot-list.html?regNumber={number}'
            item['2url'] = urlHelp,
        yield scrapy.Request(urlHelp, callback=self.ParseTable, meta={'item': item})
        #yield item
            
    '''
        if (CheckSite1):
            GenInf = {}
            for GI in response.xpath('/html/body/div[2]/div/div[2]/div/div/section'):
                Value = GI.xpath('span[2]/text()').extract_first('').strip()
                if Value:
                    GenInf[GI.xpath('span[1]/text()').extract_first('').strip() ] =  GI.xpath('span[2]/text()').extract_first('').strip()
                else:
                    GenInf[GI.xpath('span[1]/text()').extract_first('').strip() ] =  GI.xpath('span/a/text()').extract_first('').strip()
            Standart = {}
            for GI in response.xpath('/html/body/div[2]/div/div[8]/div/div/section'):
                Value = GI.xpath('span[2]/text()').extract_first('').strip()
                if Value:
                    Standart[GI.xpath('span[1]/text()').extract_first('').strip() ] =  GI.xpath('span[2]/text()').extract_first('').strip()
                else:
                    Standart[GI.xpath('span[1]/text()').extract_first('').strip() ] =  GI.xpath('span[2]/span/text()').extract_first('').strip()
            '''
            
            #for st in response.xpath('/html/body/div[2]/div/div[8]/div/div/section'):
            #    Value = st.xpath('/span[2]/text()')
            #    if Value:
            #        Standart[st.xpath('span[1]/text()').extract_first('').strip() ] =  st.xpath('/span[2]/text()').extract_first('').strip()
            #    else:
            #        Standart[st.xpath('span[1]/text()').extract_first('').strip() ] =  st.xpath('/span[2]/span[1]/text()').extract_first('').strip()
                #Standart[st.xpath('span[1]/text()').extract_first('').strip() ] =  st.xpath('/span[2]/span[1]/text()[1]').extract_first('').strip()
    '''      
            Contact ={}
            ChangeKontr = {}
            for CK in response.xpath('/html/body/div[2]/div/div[3]/div/div/section'):
                Contact[CK.xpath('span[1]/text()').extract_first('').strip() ] =  CK.xpath('span[2]/text()').extract_first('').strip()     
            item = {}
            item['номер'] = response.css('.cardMainInfo__purchaseLink ::text').extract_first('').strip()
            item['url'] = response.request.url
            item['заказчик'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/span[2]/a/text()").extract_first(' ').strip()
            item['объект'] = response.css('.cardMainInfo__content ::text').extract_first('')
            #item['начальная цена'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[1]/span[2]/text()").extract_first(' ').strip()
            #'статус закупки'] = response.css('.cardMainInfo__state ::text').extract_first('')
            item['Размещено'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span[2]/text()").extract_first(' ').strip()
            item['Обновлено'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span[2]/text()").extract_first(' ').strip()
            item['Окончание подачи заявок'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/span[2]/text()").extract_first(' ').strip()
            item['Общая информация'] = GenInf
            item['Требования'] = Standart
            item['Контактная информация'] = Contact
            yield item
    '''
        

    def ParseTable(self, response):
        item = response.meta['item']
        item['начальная цена'] = response.xpath('normalize-space(/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div/table/tbody/tr/td[4]/text())').extract_first(' ').strip()
        #item['Проверка'] = response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div/table/tbody/tr/td[4]/text()').extract_first(' ').strip()
        #head = []
        #for n  in response.xpath('/html/body/div[2]/div/div[3]/div/div/div/div[1]/table/thead/tr/th'):
            
            #head.append(n.xpath('/text()')).extract_first('').strip()
        #    item['заголовки'] = n.xpath('/text()').extract_first('').strip()

        
        yield item
    

''' 
        
            #for st in response.xpath('/html/body/div[2]/div/div[8]/div/div/section'):
            #    for s in response.xpath('/html/body/div[2]/div/div[8]/div/div/section/span[2]/span'):
            #        Standart[st.xpath('span[1]/text()').extract_first('').strip() ] =  s.xpath('/text()').extract_first('').strip()
            
            item['номер'] = response.css('.cardMainInfo__purchaseLink ::text').extract_first('').strip()
            item['url'] = res= response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/span[2]/a/text()").extract_first(' ').strip()
            #item['объект'] = rponse.request.url
            item['заказчик'] esponse.css('.cardMainInfo__content ::text').extract_first('')
            #item['начальная цена'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[1]/span[2]/text()").extract_first(' ').strip()
            #item['статус закупки'] = response.css('.cardMainInfo__state ::text').extract_first('')
            #item['Размещено'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span[2]/text()").extract_first(' ').strip()
            #item['Обновлено'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span[2]/text()").extract_first(' ').strip()
            #item['Окончание подачи заявок'] = response.xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/span[2]/text()").extract_first(' ').strip()
            #item['Общая информация'] = GenInf
            #item['Требования'] = Standart


         #url =    
        yield item
        
        elif (CheckSite2):
            GenInf = {}
            
            #GenInf[response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[1]/text()').extract_first('').strip() ] =  response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/span/text()').extract_first('').strip()
            for GI in response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr'):
                Value = GI.xpath('/td[1]/text()').extract_first('').strip()
                if Value:
                    GenInf[GI.xpath('td[1]/span/text()').extract_first('').strip() ] =  GI.xpath('td[2]/span/text()').extract_first('').strip()
                
                #else: /html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[10]/td[1]/span/text()
                #    GenInf[GI.xpath('span[1]/text()').extract_first('').strip() ] =  GI.xpath('span/a/text()').extract_first('').strip()
            
            
            
            item['номер'] = response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/span//text()").extract_first().strip(),
            item['url'] = response.request.url,
            item['заказчик'] = response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[4]/table/tbody/tr[1]/td[2]/text()').extract_first('').strip(),
            item['объект'] = response.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[4]/td[2]/span//text()').extract_first().strip()
            #item['начальная цена'] = response.xpath('//*[@id="lot"]/tbody/tr/td[4]/text()').extract_first().strip(),
            item['Размещено'] = response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[7]/td[2]/text()").extract_first(' ').strip()
            item['Обновлено'] = response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[8]/td[2]/text()").extract_first(' ').strip()
            item['Окончание подачи заявок'] = response.xpath("/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[6]/table/tbody/tr[3]/td[2]/span/text()").extract_first(' ').strip()
            item['Общая информация'] = GenInf

            

        yield item
        
'''