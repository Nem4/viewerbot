"""Find 10 working HTTP(S) proxies and save them to a file."""

import asyncio
from Proxy.proxybroker import Broker
# from proxybroker import Broker

class ProxyFinder():
    def __init__(self, nb_of_proxies):
        self.nb_of_proxies = nb_of_proxies
        self.main()

    async def save(self, proxies, filename):
        """Save proxies to a file."""
        with open(filename, 'w') as f:
            while True:
                proxy = await proxies.get()
                if proxy is None:
                    break
                proto = 'https' if 'HTTPS' in proxy.types else 'http'
                row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
                f.write(row)


    def main(self):
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS', 'SOCKS5'], limit=self.nb_of_proxies),
                               self.save(proxies, filename='Proxies_txt/scraped_proxies.txt'))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)

