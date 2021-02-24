from sqlalchemy.orm import sessionmaker
from .models import Threads, db_connect, create_table, Authors
import logging

logger = logging.getLogger(__name__)


class ThreadsPipeline(object):
    """RaidForums pipeline for storing scraped thread items in the database"""

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates threads table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save threads data in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        thread = Threads(**item)

        try:
            session.add(thread)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class AuthorsPipeline(object):
    """RaidForums pipeline for storing authors-details scraped items in the database"""

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates authors table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save authors data in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        author = Authors(**item)

        try:
            session.add(author)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
#
# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
#
# import psycopg2
#
#
# class RaidfScrapePipeline(object):
#
#     def open_spider(self, spider):
#         hostname = 'localhost'
#         username = 'postgres'
#         password = 'myagdi28273306'  # password
#         database = 'raidforums'
#         self.cur = self.connection.cursor()
#         self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
#
#     def close_spider(self, spider):
#         self.cur.close()
#         self.connection.close()
#
#     def process_item(self, item, spider):
#         # threads_data is database table name
#         self.cur.execute("insert into threads_data(title,author, date_created, last_post_by) values(%s,%s)",
#                          (item['title'], item['author'], item['date_created']), item['last_post_by'])
#         self.connection.commit()
#         return item
