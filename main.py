import scrapy


class LbcScraper(scrapy.Spider):
    name = 'lbcscraper'
    start_urls = ['https://www.leboncoin.fr/voitures/offres/p-1']

    def parse(self, response):
        root_path = 'https://www.leboncoin.fr'
        page = 0
        next_page = 'https://www.leboncoin.fr/voitures/offres/p-' + str(page)
        self.logger.info('Current page => ' + next_page)

        for car in response.css('li._3DFQ-'):
            yield {
                'name': car.css('span[data-qa-id="aditem_title"]::text').extract_first(),
                'type': car.css('p[data-qa-id="aditem_category"]::attr("content")').extract_first(),
                'location': car.css('p[data-qa-id="aditem_location"]::text').extract_first(),
                'price': car.css('span[itemprop="price"]::text').extract_first(),
                'url': root_path + car.css('a.clearfix.trackable::attr("href")').extract_first()
            }

        page += 1
        next_page = 'https://www.leboncoin.fr/voitures/offres/p-' + str(page)
        if next_page is not None and page < 11:
            yield response.follow(next_page,  self.parse())
