# -*- coding: utf-8 -*-
import scrapy
import logging
import urllib, os, re
import cfscrape
from scrapy.loader import ItemLoader
from mangadownloader.items import MangadownloaderItem
from mangadownloader.spiders.worker import download

class ComicWebIdSpider(scrapy.Spider):
    name = "comicwebid"
    allowed_domains = ["comic.web.id"]
    manga = ['Samurai_Deeper_Kyo', '39', '84']
    http = 'http://'
    base_url = 'http://comic.web.id/'
    start_urls = [
        base_url + '/'.join(manga) + '/',
    ]
    image_counter = 0
    last_chapter = manga[1]

    def parse(self, response):
        scraper = cfscrape.create_scraper()

        # create a directory
        manga_name = response.url.split('/')[3]
        chapter = response.url.split('/')[4]
        manga_info = [manga_name, manga_name + '_' + chapter]

        # Get images
        # komikid only support 1 image per page
        imgs = response.xpath('//td[@class="mid"]/table/tr[3]/td//img/@src').extract()
        # logging.info(imgs)

        if len(imgs) > 0:
            if 'http' in imgs:
                complete_image_url = imgs[0]
            else :
                complete_image_url = self.base_url + imgs[0]

            logging.info('COMPLETE IMAGE URL  = ' + complete_image_url)

            # Create local dir
            local_save_path = "downloads/comicwebid/" + '/'.join(manga_info) + '/'
            logging.info("LOCAL SAVE PATH = " + local_save_path)
            if not os.path.exists(local_save_path):
                os.makedirs(local_save_path)

            # Update image counter
            if self.last_chapter == chapter:
                self.image_counter += 1
            else:
                self.image_counter = 0
                self.last_chapter = chapter

            # Save image
            extension = complete_image_url.split('.')[-1]
            # logging.info(extension)
            local_image_path = local_save_path + '0' + str(self.image_counter) + '.' + extension
            # download.delay(complete_image_url, local_image_path)
            # urllib.urlretrieve(complete_image_url, local_image_path)
            fh = open(local_image_path, 'wb')
            fh.write(scraper.get(complete_image_url).content)
            logging.info('IMAGE SAVED TO  = ' + local_image_path)

            # Get next page
            next_page = response.xpath('//div[@class="pager"]/span[3]/a[2]/@href').extract()
            if len(next_page) > 1:
                next_page = self.base_url + next_page[0]
                # logging.info(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        else :
            # Images not found, so exit
            # os.sys.exit()
            pass