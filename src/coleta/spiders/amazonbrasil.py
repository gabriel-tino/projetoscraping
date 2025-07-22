import scrapy

class AmazonBrasilSpider(scrapy.Spider):
    name = "AmazonBrasil"
    allowed_domains = ["amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/s?k=tenis+corrida+masculino"]
    page_count = 1
    max_pages = 7

    def parse(self, response):
        products = response.css('div.s-main-slot div.s-result-item')

        for product in products:
            yield {
                'brand': product.css('span.a-size-base-plus.a-color-base::text').get(),
                'name': product.css('h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal > span::text').get(),
                'price': product.css('span.a-price-whole::text').get(),
                'cents': product.css('span.a-price-fraction::text').get(),
                'reviews_rating_number': product.css('span.a-size-base.s-underline-text::text').get(),
                'reviews_amount': product.css('span.a-icon-alt::text').get()
            }

        if self.page_count < self.max_pages:
            next_page = response.css('a.s-pagination-next::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield response.follow(url=next_page, callback=self.parse)
