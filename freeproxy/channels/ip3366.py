from freeproxy.channels import Channel


class Ip3366(Channel):
    start_urls = ['http://www.ip3366.net/']
    page = 10
    TIMEOUT = 50

    def next_page(self, url):
        while self.page_generator[url] < self.page:
            self.page_generator[url] += 1
            yield 'http://www.ip3366.net/?stype=1&page=' + str(self.page_generator[url])
