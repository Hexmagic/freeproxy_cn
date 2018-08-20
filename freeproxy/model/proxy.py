class Proxy(dict):
    def __init__(self, host, port):
        super(Proxy, self).__init__(host=host, port=port)
