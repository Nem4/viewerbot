from selenium import webdriver
import selenium
import time

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

"Define Both ProxyHost and ProxyPort as String"
ProxyHost = "95.47.76.146"
ProxyPort = 34314

def read_proxy():
    proxys = []
    f = open("proxy.txt", "r")
    f1 = f.readlines()
    for proxy in f1:
        proxy = proxy.rstrip()
        point_index = proxy.find(':')
        p_host = proxy[ : point_index]
        p_port = proxy[point_index + 1: ]
        proxys.append({'host': p_host, 'port': p_port})
    print(str(proxys))
def ChangeProxy(ProxyHost ,ProxyPort):
    """Define Firefox Profile with you ProxyHost and ProxyPort"""

    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", ProxyHost)
    profile.set_preference("network.proxy.http_port", ProxyPort)
    profile.set_preference("network.proxy.ssl", ProxyHost)
    profile.set_preference("network.proxy.ssl_port", ProxyPort)
    # driver = webdriver.Firefox(firefox_profile=profile)
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("network.proxy.type", 1)
    # profile.set_preference("network.proxy.http", ProxyHost )
    # profile.set_preference("network.proxy.http_port", int(ProxyPort))
    profile.update_preferences()
    # binary = FirefoxBinary('C:\\Users\\vlad\\PycharmProjects\\viewerbot\\geckodriver.exe')

    # Start selenium with the configured binary.
    # driver = webdriver.Firefox(firefox_binary=binary)
    return webdriver.Firefox(firefox_profile=profile, executable_path = 'geckodriver.exe')


def FixProxy():
    """"Reset Firefox Profile"""
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 0)
    return webdriver.Firefox(firefox_profile=profile)


driver = ChangeProxy(ProxyHost, ProxyPort)
driver.get("https://www.twitch.tv/agantor")

read_proxy()
# binary = FirefoxBinary('C:\\Users\\vlad\\PycharmProjects\\viewerbot\\geckodriver.exe')
# driver = webdriver.Firefox(executable_path = 'geckodriver.exe')
# driver.get("https://www.twitch.tv/agantor")

time.sleep(5)
# while True:
#     time.sleep(5)

# driver = FixProxy()
# driver.get("http://whatismyipaddress.com")