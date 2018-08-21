from freeproxy.channels import Channel


class FreeProxy(Channel):
    start_urls = ['http://free-proxy.cz/zh/proxylist/country/CN/all/ping/all']

    def next_page(self, url):
        while self.page_generator[url] < self.page:
            self.page_generator[url] += 1
            if self.page_generator[url] == 1:
                yield 'http://free-proxy.cz/zh/proxylist/country/CN/all/ping/all/'
            else:
                yield 'http://free-proxy.cz/zh/proxylist/country/CN/all/ping/all/{}'.format(self.page_generator[url])
