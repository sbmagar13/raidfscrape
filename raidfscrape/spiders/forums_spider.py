import scrapy
from raidfscrape.items import RaidfScrapeItem, AuthorScrapeItem

API_KEY = 'cfbf82b1ab2b384aa1b5582a4fc5a6b9'


class ThreadsSpider(scrapy.Spider):
    name = 'threads'

    custom_settings = {
        'ITEM_PIPELINES': {
            'raidfscrape.pipelines.ThreadsPipeline': 300,
        }
    }

    page_number = 1

    page_url = 'https://raidforums.com/Forum-Operating-Systems'

    start_urls = [f'http://api.scraperapi.com/?api_key={API_KEY}&url={page_url}&render=true']

    def parse(self, response, **kwargs):
        for thread in response.css('tr.forum-display__thread.forum-display__thread--newhotfolder.inline_row'):
            item_title = thread.css('.subject_new a span::text').get()
            item_author = thread.css('.author.smalltext a span::text').get()
            item_date_created = thread.css('.forum-display__thread-date::text').get()
            item_last_post_by = thread.css('.lastpost a span::text').get()
            item_total_replies = thread.css('.forumdisplay_regular.hidden-sm a::text').get()
            item_total_views = thread.css('.forumdisplay_regular.hidden-sm::text').get()
            item_last_post_date = thread.css('.lastpost.smalltext::text').get()
            item_author_url = thread.css('.author.smalltext a::attr(href)').get()
            threadItem = RaidfScrapeItem(title=item_title,
                                         author=item_author,
                                         author_url=item_author_url,
                                         date_created=item_date_created,
                                         last_post_by=item_last_post_by,
                                         last_post_date=item_last_post_date,
                                         total_replies=item_total_replies,
                                         total_views=item_total_views
                                         )
            yield threadItem
            print("--------------------------------------------------------------")
            print(item_author_url)
            print("--------------------------------------------------------------")

        next_page_url = f"https://raidforums.com/Forum-Operating-Systems?page={str(self.page_number)}"
        next_page = f'http://api.scraperapi.com/?api_key={API_KEY}&url={next_page_url}&render=true'

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)


class AuthorsSpider(scrapy.Spider):
    name = 'authors'

    custom_settings = {
        'ITEM_PIPELINES': {
            'raidfscrape.pipelines.AuthorsPipeline': 300,
        }
    }

    page_number = 1

    page_url = 'https://raidforums.com/Forum-Operating-Systems'

    start_urls = [f'http://api.scraperapi.com/?api_key={API_KEY}&url={page_url}&render=true']

    def parse(self, response, **kwargs):
        for thread in response.css('tr.forum-display__thread.forum-display__thread--newhotfolder.inline_row'):
            href = thread.css('.author.smalltext a::attr(href)')
            profile_url = response.urljoin(href.get())
            yield scrapy.Request(profile_url, callback=self.parse_author)

        next_page_url = f"https://raidforums.com/Forum-Operating-Systems?page={str(self.page_number)}"
        next_page = f'http://api.scraperapi.com/?api_key={API_KEY}&url={next_page_url}&render=true'

        if self.page_number <= 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response, **kwargs):
        item_name = response.css('div.profile__user-basic-info span::text').get()
        item_date_joined = response.css('div.profile__content div.profile__short-info table.tborder tr td.trow1:not('
                                        'span)::text').get()
        item_time_spent = response.css('div.profile__content div.profile__short-info table.tborder tr td:not('
                                       'span)::text')[3].get()
        item_members_referred = response.css('div.profile__content div.profile__short-info table.tborder tr '
                                             'td.trow2 a::text').get()
        # item_sex = response.css('div.profile__content div.profile__short-info tborder.tfixed trow1.scaleimages:not('
        #                         'span)::text').get()
        item_total_threads = response.css('div.profile__content div.profile__main-info table tr td div.d-table.w-100 '
                                          'div::text')[1].re(r'\d+')[0]
        item_total_posts = response.css('div.profile__content div.profile__main-info table tr td div.d-table.w-100 '
                                        'div::text')[4].re(r'\d+')[0]
        item_reputation = response.css('div.profile__content div.profile__main-info table tr td div strong::text').get()

        authorItem = AuthorScrapeItem(name=item_name,
                                      date_joined=item_date_joined,
                                      time_spent=item_time_spent,
                                      members_referred=item_members_referred,
                                      # sex=item_sex,
                                      total_threads=item_total_threads,
                                      total_posts=item_total_posts,
                                      reputation=item_reputation
                                      )
        yield authorItem
