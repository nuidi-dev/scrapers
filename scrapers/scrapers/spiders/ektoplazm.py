# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapers.items import EktoSongItem

class EktoplazmSpider(scrapy.Spider):

    name = "ektoplazm"
    allowed_domains = ["ektoplazm.com"]
    start_urls = ['http://www.ektoplazm.com/']

    def parse(self, response):
        requests = []
        styles = response.css('div#sidemenu div a:not([href="/donate"])')
        for style in styles:
            style_name = style.css('::text').extract()[0]
            style_link = style.css('::attr(href)').extract()[0]
            r = Request(style_link, callback=self.parse_style)
            requests.append(r)

        return requests

    def parse_style(self, response):

        item = EktoSongItem()
        albums = response.css('.post')

        for album in albums:
            item['album_name'] = album.css('h1 a::text').extract()[0]
            item['album_link'] = album.css('h1 a::attr(href)').extract()[0]
            styles = album.css('h3 span.style')
            for s in styles:
                styles_string = ', '.join(s.css('strong a::text').extract())
            item['album_styles'] = styles_string

            item['album_added_time'] = album.css('h3 span.d::text').extract()[0]

            try:
                item['album_added_by'] = album.css('h3 a[rel="author external"]::text').extract()[0]
            except IndexError:
                pass

            try:
                item['album_released_by'] = album.css('h3 strong a[rel="tag"]::text').extract()[0]
            except IndexError:
                pass

            item['album_download_count'] = str(album.css('div.entry span.dc strong::text').extract()[0].replace(',' ,''))

            dl_links = album.css('div.entry span.dll a::attr(href)')

            try:
                item['album_download_link_1'] = dl_links[0].extract()
            except IndexError:
                pass

            try:
                item['album_download_link_2'] = dl_links[1].extract()
            except IndexError:
                pass

            try:
                item['album_download_link_3'] = dl_links[2].extract()
            except IndexError:
                pass

            rating = album.css('p.postmetadata span.d strong::text')
            item['album_rating'] = rating[0].extract()
            item['album_votes_count'] = rating[1].extract()

            songs_counter = len(album.css('.entry .tl .n'))
            songs_container = album.css('.entry .tl')

            for s_c in range(0, songs_counter):

                song_item = item

                try:
                    song_title = songs_container.css('span.t::text').extract()[s_c]
                except IndexError:
                    continue

                try:
                    song_bpm = songs_container.css('span.d::text').extract()[s_c]
                    song_item['song_bpm'] = song_bpm.replace("BPM", "").strip("()")
                except IndexError:
                    pass

                song_item['song_title'] = song_title

                yield song_item

        last_page_number = int(response.css('.navigation .wp-pagenavi span.pages::text').extract()[0].split(" ")[-1])

        if 'pagenum' not in response.meta:
            for page_num in xrange(2, last_page_number+1):
                yield Request(response.request.url+"/page/{}".format(page_num,), callback=self.parse_style, meta={'pagenum': page_num})
