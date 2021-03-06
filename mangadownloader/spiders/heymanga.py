# -*- coding: utf-8 -*-
import scrapy
import logging
import urllib, os, re
from scrapy.loader import ItemLoader
from mangadownloader.items import MangadownloaderItem
from mangadownloader.spiders.worker import download

class HeymangaSpider(scrapy.Spider):
    name = "heymanga"
    allowed_domains = ["heymanga.me"]
    # manga = [
    #     ['Kingdom', '499', '1'],
    # ]
    manga = ['Kingdom', '500', '1']
    start_urls = [
        'https://www.heymanga.me/manga/' + '/'.join(manga),
    ]
    https = 'https://'
    base_url = 'https://www.heymanga.me'
    image_counter = 0
    last_chapter = manga[1]

    def parse(self, response):
        # create a directory
        manga_name = response.url.split('/')[4]
        chapter = response.url.split('/')[5]
        manga_info = [manga_name, manga_name + '_' + chapter]

        # Get images
        imgs = response.xpath('//img[@class="img-fill"]/@src')

        if len(imgs) > 0:
            # Create local dir
            local_save_path = "downloads/" + '/'.join(manga_info) + '/'
            if not os.path.exists(local_save_path):
                os.makedirs(local_save_path)
        else :
            # Images not found, so exit
            # os.sys.exit()
            pass

        for img in imgs:
            image = img.extract()
            # Append url
            complete_image_url = self.https + image[2:]
            #logging.info(complete_image_url)

            # Update image counter
            if self.last_chapter == chapter:
                self.image_counter += 1
            else:
                self.image_counter = 0
                self.last_chapter = chapter

            # Save image
            file_name = complete_image_url.split('/')[-1]
            extension = complete_image_url.split('.')[-1]
            local_image_path = local_save_path + '0' + str(self.image_counter) + '.' + extension
            download.delay(complete_image_url, local_image_path)
            #logging.info('Image saved to ' + local_image_path)

        # Get next page
        next_page = response.xpath('//a[@class="btn btn-sm"]/@href').extract()
        if len(next_page) > 1:
            next_page = next_page[-1]
            next_page = self.base_url + next_page
            logging.info(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

