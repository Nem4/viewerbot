from selenium import webdriver
import time

from Other.getproxy import GetProxy

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
    return proxys
def ChangeProxy(ProxyHost ,ProxyPort):
    """Define Firefox Profile with you ProxyHost and ProxyPort"""

    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("network.proxy.type", 1)
    # profile.set_preference("network.proxy.http", ProxyHost)
    # profile.set_preference("network.proxy.http_port", ProxyPort)
    # profile.set_preference("network.proxy.ssl", ProxyHost)
    # profile.set_preference("network.proxy.ssl_port", ProxyPort)
    # driver = webdriver.Firefox(firefox_profile=profile)

    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("network.proxy.type", 1)
    # profile.set_preference("network.proxy.http", ProxyHost )
    # profile.set_preference("network.proxy.http_port", int(ProxyPort))
    # profile.update_preferences()

    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    #
    # # Proxy IP & Port
    # prox.http_proxy = f"{ProxyHost}:{ProxyPort}"
    # prox.socks_proxy = f"{ProxyHost}:{ProxyPort}"
    # prox.ssl_proxy = f"{ProxyHost}:{ProxyPort}"
    #
    # # Configure capabilities
    # capabilities = webdriver.DesiredCapabilities.FIREFOX
    # prox.add_to_capabilities(capabilities)
    #
    # # Configure ChromeOptions
    # driver = webdriver.Firefox(desired_capabilities=capabilities)
    # # binary = FirefoxBinary('C:\\Users\\vlad\\PycharmProjects\\viewerbot\\geckodriver.exe')
    #
    # # Start selenium with the configured binary.
    # # driver = webdriver.Firefox(firefox_binary=binary)
    # driver.get("http://www.whatsmyip.org/")
    # # return webdriver.Firefox(firefox_profile=profile)
    # return webdriver.Firefox(desired_capabilities=capabilities)

    http_proxy = f"{ProxyHost}:{ProxyPort}"
    https_proxy = f"{ProxyHost}:{ProxyPort}"
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": http_proxy,
        "sslProxy": https_proxy,
        "proxyType": "MANUAL"
    }
    return webdriver.Firefox()
    # driver = webdriver.Firefox()
    # driver.get("http://www.whatsmyip.org/")



def FixProxy():
    """"Reset Firefox Profile"""
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 0)
    return webdriver.Firefox(firefox_profile=profile)

gp = GetProxy()
gp.get_proxy()

url = 'https://whatismyipaddress.com/'
url = 'https://www.twitch.tv/agantor'
for proxy in read_proxy():
    driver = None
    try:
        host = proxy['host']
        port = proxy['port']
        print(f"current proxy: {host}:{port}")
        driver = ChangeProxy(host, port)
        # driver.get("https://www.twitch.tv/al_twitch_123")
        driver.get(url)
        time.sleep(1)
        try:
            # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'T')
            # driver.execute_script("window.open('');")
            driver.execute_script(f'window.open("{url}","_blank");')
            # driver.get('https://whatismyipaddress.com/')
        except:
            print("Cant open new tab")
            driver.close()


    except:
        print("Broken proxy")
        time.sleep(3)
        driver.close()
    # driver.get('https://whatismyipaddress.com/')
    time.sleep(3)

# read_proxy()
# binary = FirefoxBinary('C:\\Users\\vlad\\PycharmProjects\\viewerbot\\geckodriver.exe')
# driver = webdriver.Firefox(executable_path = 'geckodriver.exe')
# driver.get("https://www.twitch.tv/agantor")

time.sleep(5)
# while True:
#     time.sleep(5)

# driver = FixProxy()
# driver.get("http://whatismyipaddress.com")