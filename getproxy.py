from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random


class GetProxy():

    def __init__(self, delete_proxy = False):
        self.ua = UserAgent()  # From here we generate a random user agent
        self.proxies = []  # Will contain self.proxies [ip, port]
        if delete_proxy:
            import os
            if os.path.exists("proxy_list.txt"):
                os.remove("proxy_list.txt")

    # Main function
    def get_proxy(self):
        # Retrieve latest self.proxies
        proxies_req = Request('https://www.sslproxies.org/')
        proxies_req.add_header('User-Agent', self.ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')

        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        # Save self.proxies in the array
        for row in proxies_table.tbody.find_all('tr'):
            self.proxies.append({
                'ip': row.find_all('td')[0].string,
                'port': row.find_all('td')[1].string
            })

        proxies_req = Request('http://spys.me/proxy.txt')
        proxies_req.add_header('User-Agent', self.ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')

        soup = BeautifulSoup(proxies_doc, 'html.parser').text
        # proxies_table = soup.find('pre')
        # print("******START******")
        all_proxies = soup[216: -69]
        all_lines = all_proxies.splitlines()
        for line in all_lines:
            host = line[: line.find(':')]
            port = line[line.find(':') + 1:line.find(' ')]
            self.proxies.append({
                'ip': host,
                'port': port
            })

        proxies_req = Request('https://proxy.rudnkh.me/txt')
        proxies_req.add_header('User-Agent', self.ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')

        soup = BeautifulSoup(proxies_doc, 'html.parser').text
        # proxies_table = soup.find('pre')
        # print("******START******")
        all_proxies = soup
        all_lines = all_proxies.splitlines()
        for line in all_lines:
            # print(line[len(line)-2: ].strip())
            if line[len(line) - 2:].strip() == "+":
                host = line[: line.find(':')]
                port = line[line.find(':') + 1:line.find(' ')]
                self.proxies.append({
                    'ip': host,
                    'port': port
                })

                # print(f"host #: {line[ : line.find(':')]}")
                # print(f"port #: {line[line.find(':') + 1:line.find(' ') ]}")
        # print(all_proxies)
        # print("******END******")
        for p in self.proxies:
            self.save_proxy(p['ip'], p['port'])
        # Choose a random proxy
        # proxy_index = self.random_proxy()
        # proxy = self.proxies[proxy_index]
        # already_saved = False
        # for n in range(1, 100):
        #     req = Request('http://icanhazip.com')
        #     req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
        #
        #     # Every 10 requests, generate a new proxy
        #     if n % 3 == 0:
        #         proxy_index = self.random_proxy()
        #         proxy = self.proxies[proxy_index]
        #         already_saved = False
        #
        #     # Make the call
        #     try:
        #         my_ip = urlopen(req).read().decode('utf8')
        #         print('#' + str(n) + ': ' + my_ip)
        #         if n % 2 == 0 and already_saved == False:
        #             self.save_proxy(proxy['ip'], proxy['port'])
        #             already_saved = True
        #     except:  # If error, delete this proxy and find another one
        #         del self.proxies[proxy_index]
        #         print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
        #         proxy_index = self.random_proxy()
        #         proxy = self.proxies[proxy_index]

    # Retrieve a random index proxy (we need the index to delete it if not working)
    def random_proxy(self):
        return random.randint(0, len(self.proxies) - 1)

    def save_proxy(self, proxy_host, proxy_port):
        proxys = open("proxy_list.txt", "a+")
        proxys.write(f"{proxy_host}:{proxy_port}" + '\n')


gp = GetProxy()
gp.get_proxy()
