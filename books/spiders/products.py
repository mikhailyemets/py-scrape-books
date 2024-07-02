import scrapy
from scrapy.http import Response


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response: Response, **kwargs):
        for product in response.css("article.product_pod"):
            detail_page_url = product.css("h3 a::attr(href)").get()
            if detail_page_url:
                yield response.follow(detail_page_url, callback=self.parse_detail)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response: Response):
        yield {
            "title": response.css("div.product_main h1::text").get(),
            "price": response.css("p.price_color::text").get().replace("£", ""),
            "amount_in_stock": response.css("p.availability::text").re_first("\d+"),
            "rating": response.css("p.star-rating::attr(class)").re_first("star-rating (\w+)"),
            "category": response.css("ul.breadcrumb li:nth-child(3) a::text").get(),
            "description": response.css("div#product_description ~ p::text").get(),
            "upc": response.css("table.table tr:nth-child(1) td::text").get(),
        }
