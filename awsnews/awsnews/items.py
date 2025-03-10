# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AwsnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):
    article_id = scrapy.Field()

    title = scrapy.Field()
    url = scrapy.Field()
    date_published = scrapy.Field()
    author = scrapy.Field()
    lead = scrapy.Field()
    content = scrapy.Field()
    html_content = scrapy.Field()

    tags = scrapy.Field()
    section = scrapy.Field()
    image_urls = scrapy.Field()
    source = scrapy.Field()
    scraped_date = scrapy.Field()
    language = scrapy.Field()
    keywords = scrapy.Field()

    def __repr__(self):
        formatted = "{\n"
        for key in ["title", "url", "date_published", "author", "tags", "keywords"]:
            formatted += f"  {repr(key)}: {repr(self.get(key))},\n"
        formatted += "}"
        return formatted