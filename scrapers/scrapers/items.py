# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class EktoSongItem(scrapy.Item):
    album_name = scrapy.Field()
    album_link = scrapy.Field()
    album_styles = scrapy.Field()
    album_added_time = scrapy.Field()
    album_added_by = scrapy.Field()
    album_released_by = scrapy.Field()
    album_download_count = scrapy.Field()
    album_rating = scrapy.Field()
    album_votes_count = scrapy.Field()

    album_download_link_1 = scrapy.Field()
    album_download_link_2 = scrapy.Field()
    album_download_link_3 = scrapy.Field()

    # song_number = scrapy.Field()
    song_title = scrapy.Field()
    song_bpm = scrapy.Field()
