# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


class RaidfScrapeItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    date_created = scrapy.Field()
    last_post_by = scrapy.Field()
    last_post_date = scrapy.Field()
    total_replies = scrapy.Field()
    total_views = scrapy.Field()


class AuthorScrapeItem(scrapy.Item):
    name = scrapy.Field()
    # sex = scrapy.Field()
    date_joined = scrapy.Field(
        input_processor=MapCompose(str.strip),
        outpu_processor=TakeFirst()
    )
    time_spent = scrapy.Field(
        input_processor=MapCompose(str.strip),
        outpu_processor=TakeFirst()
    )
    members_referred = scrapy.Field(
        input_processor=MapCompose(str.strip),
        outpu_processor=TakeFirst()
    )
    total_threads = scrapy.Field(
        input_processor=MapCompose(str.strip),
        outpu_processor=TakeFirst()
    )
    total_posts = scrapy.Field(
        input_processor=MapCompose(str.strip),
        outpu_processor=TakeFirst()
    )
    reputation = scrapy.Field(
        input_processor=MapCompose(str.strip),
        outpu_processor=TakeFirst()
    )
