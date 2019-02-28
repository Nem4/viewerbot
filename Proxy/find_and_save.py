"""Find 10 working HTTP(S) proxies and save them to a file."""

import asyncio
from Proxy.proxybroker import Broker
import sys
import linecache
# from proxybroker import Broker


def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

class ProxyFinder():
    def __init__(self, nb_of_proxies = None):
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
        if self.nb_of_proxies == None:
            tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS']),
                               self.save(proxies, filename='Proxies_txt/scraped_proxies.txt'))
        else:
            tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=self.nb_of_proxies),
                                   self.save(proxies, filename='Proxies_txt/scraped_proxies.txt'))
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(tasks)
        except:
            print_exception()
