'''
Copyright 2015 ohyou
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import requests
from livestreamer import Livestreamer
import sys
# import multiprocessing
import time
import random
from random import shuffle
from fake_useragent import UserAgent
# from itertools import product
# from multiprocessing.dummy import Pool as ThreadPool
import linecache

from threading import Thread


channel_url = "https://www.twitch.tv/agantor"
# channel_url = "https://www.twitch.tv/mgberg"
# channel_url = "twitch.tv/piggyesgames"
# channel_url = "https://www.twitch.tv/spirit_stan"
# channel_url = "https://www.twitch.tv/" + sys.argv[1]
# channel_url = "https://www.twitch.tv/al_twitch_123"
channel_url = "https://www.twitch.tv/comboedow"
proxies_file = "Proxies_txt/good_proxy.txt"
processes = []
max_viewers = 500
max_nb_of_threads = 5000
# all_processes = []
nb_of_proxies = 0
ua = UserAgent()
# url = None
all_proxies = []
session = Livestreamer()
session.set_option("http-headers", {'User-Agent': ua.random, "Client-ID": "ewvlchtxgqq88ru9gmfp1gmyt6h2b93"})
# from Proxy.find_and_save import ProxyFinder
# pf = ProxyFinder(2000)
# sys.exit(0)


def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def get_channel():
    # Reading the channel name - passed as an argument to this script
    if len(sys.argv) >= 2:
        global channel_url
        channel_url += sys.argv[1]
    else:
        print("An error has occurred while trying to read arguments. Did you specify the channel?")
        sys.exit(1)


def get_proxies():
    # Reading the list of proxies
    global nb_of_proxies
    try:
        lines = [line.rstrip("\n") for line in open(proxies_file)]
    except IOError as e:
        print("An error has occurred while trying to read the list of proxies: %s" % e.strerror)
        sys.exit(1)

    nb_of_proxies = len(lines)
    return lines


def get_url():
    url = ""
    try:
        streams = session.streams(channel_url)
        # print(str(streams))
        try:
            url = streams['audio_only'].url
        except:
            url = streams['worst'].url
    except:
        print("Wasnt able to get url")
    return url

def open_url(proxy_data):
    # global url
    try:
        global all_proxies
        # print(f"URL: {url}")
        # print(f"PAssed proxy: {proxy}")
        # current_proxy = {"http": proxy}
        # current_proxy = proxy
        # print("Proxy: " + current_proxy)
        headers = {'User-Agent': ua.random}
        current_index = all_proxies.index(proxy_data)

        if proxy_data['url'] == "":
            proxy_data['url'] = get_url()
            # all_proxies[current_index] = proxy_data
        current_url = proxy_data['url']
        # print(str(current_url))
        try:
             if time.time() - proxy_data['time'] >= random.randint(1, 5):
                # url = get_url()
                current_proxy = {"http": proxy_data['proxy'], "https": proxy_data['proxy']}
                with requests.Session() as s:
                    response = s.head(current_url, proxies=current_proxy, headers=headers)
                print(f"Sent HEAD request with {current_proxy['http']} | {response.status_code} | {response.request} | {response}")
                # if response.status_code != 200:
                #     all_proxies.pop(current_index)
                proxy_data['time'] = time.time()
                all_proxies[current_index] = proxy_data
        except:
            print("************* Connection Error! *************")
            # print_exception()
            # all_proxies.remove(proxy_data)
            # try:
            #     all_proxies.pop(current_index)
            # except:
            #     print("Wasnt able to remove proxy")
    except (KeyboardInterrupt, SystemExit):
        # cleanup_stop_thread()
        sys.exit()

if __name__ == "__main__":
    start_time = time.time()
    # for i in range(0, 5):
    #     print(str(get_url()))
    # url = get_url()
    proxies = get_proxies()
    
    for p in proxies:
        all_proxies.append({'proxy': p, 'time': time.time(), 'url': ""})

    shuffle(all_proxies)
    list_of_all_proxies = all_proxies
    current_proxy_index = 0
    
    # while True:
    #     try:
    #         if current_proxy_index >= len(all_proxies):
    #             current_proxy_index = 0
    #         if time.time() - list_of_all_proxies[current_proxy_index]['time'] >= random.randint(7, 20): 
    #             current_proxy = list_of_all_proxies[current_proxy_index]['proxy']
    #             # print(f"Current proxy: {current_proxy}")
    #             pool = ThreadPool(10)
    #             results = pool.starmap(open_url, [({"http": current_proxy}, url)])
    #             if results is not True:
    #                 all_proxies.pop(current_proxy_index)
    #             current_proxy_index += 1
    #             list_of_all_proxies[current_proxy_index]['time'] = time.time()
    #     except:
    #         print(str(sys.exc_info()))
    #         sys.exit(1)


    while True:
        # if time.time() - start_time > 180:
        #     for proxy in all_proxies:
        #         print(str(proxy['proxy']))
        #     break
        try:
            for i in range(0, max_nb_of_threads):
                threaded = Thread(target=open_url, args=(all_proxies[random.randint(0, len(all_proxies))],))
                threaded.daemon = True  # This thread dies when main thread (only non-daemon thread) exits.
                threaded.start()
            # print(f"Current proxy: {current_proxy}")
            # pool = ThreadPool(1000)
            # pool.set
            # results = pool.map(open_url, all_proxies)
        except:
            # print(str(sys.exc_info()))
            print_exception()
        shuffle(all_proxies)
        time.sleep(1)
            # sys.exit(1)
        # nb = 0
        # # time.sleep(random.randint(1, 2))
        # for p in processes:
        #     if p.is_alive():
        #         nb+=1
        # print(f"Running {nb} of {max_viewers}")
        # time.sleep(1)
