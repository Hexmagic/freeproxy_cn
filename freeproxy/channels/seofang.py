from freeproxy.channels import Channel


class SeoFang(Channel):
    start_urls = ['http://ip.seofangfa.com/']

    def next_page(self, url):
        yield url
