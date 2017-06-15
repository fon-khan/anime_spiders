# coding: utf-8
from urllib import urlencode
from urlparse import urlparse, parse_qs

from scrapy import Spider, Request

from anime_spiders.items import Anime


class BangumiSpider(Spider):
    name = 'bangumi'
    start_urls = [
        'http://bangumi.tv/anime/browser/?sort=date&page=1',
    ]
    base_url = 'http://bangumi.tv/anime/browser/'
    custom_settings = {
        'ITEM_PIPELINES': {
            'anime_spiders.pipelines.BangumiTVCoverPipeline': 100,
            'anime_spiders.pipelines.AnimeTagsPipeline': 150,
            'anime_spiders.pipelines.DjangoItemPipeline': 200,
        }
    }

    def parse(self, rsp):
        subjects = rsp.xpath('//ul[@id="browserItemList"]/li')
        if not subjects:
            return
        for s in subjects:
            link = s.xpath('a/@href').extract_first()
            details_path = 'http://bangumi.tv%s' % link

            yield Request(details_path, callback=self.parse_details)

        next_url = self.get_next_url(rsp)
        yield Request(next_url, callback=self.parse)

    def parse_details(self, rsp):
        infobox = rsp.xpath('//ul[@id="infobox"]')[0]
        try:
            episodes = int(infobox.xpath(u'//span[contains(text(),"话数:")]/ancestor::li/text()').extract_first())
        except:
            episodes = None

        return Anime(
            crawled_from='bangumi.tv',
            site_pk=int(rsp.url.replace('http://bangumi.tv/subject/', '')),
            episodes=episodes,
            link=rsp.url,
            cover=rsp.xpath('//div[@class="infobox"]/div/a/@href').extract_first(),
            name=infobox.xpath(u'//span[contains(text(),"中文名:")]/ancestor::li/text()').extract_first(),
            orig_name=rsp.xpath('//div[@class="infobox"]/div/a/@title').extract_first(),

            pub_date=infobox.xpath(u'//span[contains(text(),"放送开始:")]/ancestor::li/text()').extract_first(),
            alter_names=infobox.xpath(u'//span[contains(text(),"别名:")]/ancestor::li/text()').extract(),

            directors=infobox.xpath(u'//span[contains(text(),"导演")]/ancestor::li/a/text()').extract(),
            scenarists=infobox.xpath(u'//span[contains(text(),"脚本:")]/ancestor::li/a/text()').extract(),
            company=infobox.xpath(u'//span[contains(text(),"动画制作")]/ancestor::li/a/text()').extract(),
            assit_companies=infobox.xpath(u'//span[contains(text(),"制作助手")]/ancestor::li/a/text()').extract(),
            effect_makers=infobox.xpath(u'//span[contains(text(),"特效")]/ancestor::li/a/text()').extract(),
            audio_directors=infobox.xpath(u'//span[contains(text(),"音响监督")]/ancestor::li/a/text()').extract(),
            main_animators=infobox.xpath(u'//span[contains(text(),"原画")]/ancestor::li/a/text()').extract(),
            photo_directors=infobox.xpath(u'//span[contains(text(),"摄影监督")]/ancestor::li/a/text()').extract(),
            mechanical_designers=infobox.xpath(u'//span[contains(text(),"机械设定")]/ancestor::li/a/text()').extract(),
            anime_directors=infobox.xpath(u'//span[contains(text(),"作画监督")]/ancestor::li/a/text()').extract(),
            charactor_designers=infobox.xpath(u'//span[contains(text(),"人物设定")]/ancestor::li/a/text()').extract(),
            musicians=infobox.xpath(u'//span[contains(text(),"音乐:")]/ancestor::li/a/text()').extract(),
            storyboard_directors=infobox.xpath(u'//span[contains(text(),"分镜构图")]/ancestor::li/a/text()').extract(),
            acts=infobox.xpath(u'//span[contains(text(),"演出:")]/ancestor::li/a/text()').extract(),
        )

    def get_next_url(self, rsp):
        current_url = rsp.url
        parsed_url = urlparse(current_url)
        args = parse_qs(parsed_url.query)
        page = int(args['page'][0]) + 1
        next_url = '{}?{}'.format(self.base_url,
                                  urlencode(dict(sort='date', page=page)))
        return next_url

    def get_full_url(self, url):
        return 'http:%s' % url
