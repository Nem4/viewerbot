import requests
from livestreamer import Livestreamer
import sys
import time
import random
from random import shuffle
from fake_useragent import UserAgent
import linecache

from threading import Thread

channel_url = ""
proxies_file = "Proxies_txt/good_proxy.txt"
processes = []
max_nb_of_threads = 1000

all_proxies = []
nb_of_proxies = 0

# Session creating for request
ua = UserAgent()
session = Livestreamer()
session.set_option("http-headers", {'User-Agent': ua.random, "Client-ID": "ewvlchtxgqq88ru9gmfp1gmyt6h2b93"})


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
        try:
            url = streams['audio_only'].url
        except:
            url = streams['worst'].url
    except:
        print("Wasnt able to get url")
    return url

def open_url(proxy_data):
    try:
        global all_proxies
        headers = {'User-Agent': ua.random}
        current_index = all_proxies.index(proxy_data)

        if proxy_data['url'] == "":
            proxy_data['url'] = get_url()
        current_url = proxy_data['url']
        try:
             if time.time() - proxy_data['time'] >= random.randint(1, 5):
                current_proxy = {"http": proxy_data['proxy'], "https": proxy_data['proxy']}
                with requests.Session() as s:
                    response = s.head(current_url, proxies=current_proxy, headers=headers)
                print(f"Sent HEAD request with {current_proxy['http']} | {response.status_code} | {response.request} | {response}")
                proxy_data['time'] = time.time()
                all_proxies[current_index] = proxy_data
        except:
            print("************* Connection Error! *************")

    except (KeyboardInterrupt, SystemExit):
        sys.exit()


if __name__ == "__main__":

    if len(sys.argv) == 1:
        channel_url = "https://www.twitch.tv/" + sys.argv[1]
    else:
        channel_url = "https://www.twitch.tv/your_channel_name"
    start_time = time.time()
    proxies = get_proxies()
    
    for p in proxies:
        all_proxies.append({'proxy': p, 'time': time.time(), 'url': ""})

    shuffle(all_proxies)
    list_of_all_proxies = all_proxies
    current_proxy_index = 0

    while True:
        try:
            for i in range(0, max_nb_of_threads):
                threaded = Thread(target=open_url, args=(all_proxies[random.randint(0, len(all_proxies))],))
                threaded.daemon = True  # This thread dies when main thread (only non-daemon thread) exits.
                threaded.start()
        except:
            print_exception()
        shuffle(all_proxies)
        time.sleep(5)
