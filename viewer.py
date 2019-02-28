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
import subprocess
import json
import sys
import multiprocessing
import time
import random
from random import shuffle
from fake_useragent import UserAgent

channel_url = "twitch.tv/agantor"
# channel_url = "https://www.twitch.tv/mgberg"
# channel_url = "twitch.tv/piggyesgames"
# channel_url = "https://www.twitch.tv/spirit_stan"
channel_url = "https://www.twitch.tv/" + sys.argv[1]
proxies_file = "Proxies_txt/good_proxy.txt"
processes = []
max_viewers = 500
# all_processes = []
nb_of_proxies = 0
ua = UserAgent()
# from Proxy.find_and_save import ProxyFinder
# pf = ProxyFinder(2000)
# sys.exit(0)

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
    # Getting the json with all data regarding the stream
    try:
        response = subprocess.Popen(
            ["livestreamer.exe", "--http-header", "Client-ID=ewvlchtxgqq88ru9gmfp1gmyt6h2b93",
            channel_url, "-j"], stdout=subprocess.PIPE).communicate()[0]
    except subprocess.CalledProcessError:
        print("An error has occurred while trying to get the stream data. Is the channel online? Is the channel name correct?")
        sys.exit(1)
    except OSError:
        print("An error has occurred while trying to use livestreamer package. Is it installed? Do you have Python in your PATH variable?")

    # Decoding the url to the worst quality of the stream
    try:
        url = json.loads(response)['streams']['audio_only']['url']
    except:
        try:
            url = json.loads(response)['streams']['worst']['url']
        except (ValueError, KeyError):
            print("An error has occurred while trying to get the stream data. Is the channel online? Is the channel name correct?")
            sys.exit(1)

    return url


def open_url(proxy, all_proxies):
    # Sending HEAD requests
    shuffle(all_proxies)
    nb_of_tries = 0
    nb_of_proxies_failures = 0
    url = get_url()
    max_proxy_failure = 20
    # url = get_url()
    # time.sleep(random.randint(4, 15))
    current_proxy = proxy
    while True:
        headers = {
            'User-Agent': ua.random
        }
        try:
            with requests.Session() as s:
                response = s.head(url, proxies=current_proxy, headers=headers)
            print(f"Sent HEAD request with {current_proxy['http']} | {response.status_code} | {response.request} | {response}")
            if response.status_code == 503:
                nb_of_tries += 1
                # print("  SERVICE UNAVAILABLE %s" % proxy["http"])
                if nb_of_tries > 1:
                    if nb_of_proxies_failures > max_proxy_failure:
                        print("################### Closing this thread! ################### ")
                        break
                    else:
                        print("################### CHANGING PROXY ################### ")
                        current_proxy = {"http": all_proxies[0]}
                        nb_of_proxies_failures += 1
            time.sleep(20)
        except requests.exceptions.Timeout:
            nb_of_tries += 1
            print("  Timeout error for %s" % current_proxy["http"])
            if nb_of_tries > 1:
                if nb_of_proxies_failures > max_proxy_failure:
                    print("################### Closing this thread! ################### ")
                    break
                else:
                    print("################### CHANGING PROXY ################### ")
                    current_proxy = {"http": all_proxies[0]}
                    nb_of_proxies_failures += 1
        except requests.exceptions.ConnectionError:
            nb_of_tries += 1
            print("  Connection error for %s" % current_proxy["http"])
            if nb_of_tries > 1:
                if nb_of_proxies_failures > max_proxy_failure:
                    print("################### Closing this thread! ################### ")
                    break
                else:
                    print("################### CHANGING PROXY ################### ")
                    current_proxy = {"http": all_proxies[0]}
                    nb_of_proxies_failures += 1


def prepare_processes():
    global processes
    proxies = get_proxies()
    shuffle(proxies)
    if len(proxies) < 1:
        print("An error has occurred while preparing the process: Not enough proxy servers. Need at least 1 to function.")
        sys.exit(1)

    n = 0
    for proxy in proxies:
        if n<max_viewers:
            # Preparing the process and giving it its own proxy
            # processes.append(
            #     multiprocessing.Process(
            #         target=open_url, kwargs={"all_proxies": proxies,
            #             "proxy": {
            #                 "http": proxy}}))
            p = multiprocessing.Process(
                    target=open_url, kwargs={"all_proxies": proxies,
                                             "proxy": {
                                                 "http": proxy}})
            p.daemon = True
            p.start()

            n += 1
            print(f'Prepearing # {n} of {len(proxies)}')
        else:
            break
    print(f"Max viewers: {len(proxies)}")
    print('')

if __name__ == "__main__":
    print("Obtaining the channel...")
    # get_channel()
    print("Obtained the channel")
    print("Preparing the processes...")
    prepare_processes()
    print("Prepared the processes")
    print("Booting up the processes...")

    # Timer multiplier
    # n = 8

    # Starting up the processes
    # for process in processes:
    #     time.sleep(random.randint(1, 2))
    #     process.daemon = True
    #     process.start()
    #     if n > 1:
    #         n -= 1

    # Running infinitely
    while True:
        # nb = 0
        # # time.sleep(random.randint(1, 2))
        # for p in processes:
        #     if p.is_alive():
        #         nb+=1
        # print(f"Running {nb} of {max_viewers}")
        time.sleep(1)