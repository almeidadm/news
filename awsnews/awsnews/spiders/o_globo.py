from typing import Any
import scrapy
from scrapy.spiders import SitemapSpider

from awsnews.items import NewsItem


class OGloboSpider(SitemapSpider):
    name = "o_globo"
    allowed_domains = ["oglobo.globo.com"]
    sitemap_urls = ['https://oglobo.globo.com/sitemap/oglobo/sitemap.xml']
    sitemap_follow = ['/sitemap/', '/noticias/']

#    sitemap_rules = [
#        ('/noticias/', 'parse_article'),
#        ('/sitemap/', 'parse_sitemap'),
#    ]
    def parse_sitemap(self, response):
        # Extraímos todas as URLs do sitemap
        for url in response.css("url loc::text").getall():
            print(f"Found sitemap URL: {url}")
            yield scrapy.Request(url, callback=self.parse_sitemap if "sitemap" in url else self.parse_article)

    def parse(self, response):
        # A função parse_article extrai as informações da página de artigo
        
        yield NewsItem(
            title=response.css('h1[itemprop="headline"]::text').get(),  # Melhor usar get() ao invés de extract_first()
            url=response.url,
            date_published=response.css('time[itemprop="datePublished"]::attr(datetime)').get(),#.attrib["datetime"],
            author=response.css('meta[itemprop="name"]::attr(content)').get(),
            lead=response.css('h2[itemprop="alternativeHeadline"]::text').get(),
            content=" ".join(response.css('div p.content-text__container::text').getall()),
            # html_content=str(response.body),
            tags=response.css(".bread-crumb-title a::text").getall(),
            image_urls=[item.attrib['src'] for item in response.css("#oglobo img")],
            source=response.css('meta[property="og:site_name"]').attrib["content"],
            keywords=response.css('meta[name="keywords"]').attrib.get("content", ""),
        )
