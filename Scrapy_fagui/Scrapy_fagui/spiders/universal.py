from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import get_config

class UniversalSpider(CrawlSpider):
    name = 'universal'

    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains')
        rules = []
        for rule_kwargs in config.get('rules'):
            link_extractor = LinkExtractor(**rule_kwargs.get('link_extractor'))
            rule_kwargs['link_extractor'] = link_extractor
            rule = Rule(**rule_kwargs)
            rules.append(rule)
        self.rules = rules
        super(UniversalSpider, self).__init__(*args, **kwargs)