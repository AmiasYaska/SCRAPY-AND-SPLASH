# spiders/quotes.py

import scrapy
from scrapy_splash import SplashRequest


lua_script = """
function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0
    
    splash.images_enabled = false

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end        
    return splash:html()
end


"""

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/scroll'
        yield SplashRequest(
            url,
            callback=self.parse,
            endpoint='execute',
            args={'wait': 0.5, 'lua_source': lua_script,  url:'https://quotes.toscrape.com/scroll'}
            )

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall()
            }

