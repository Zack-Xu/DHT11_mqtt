import network


def do_connect(essid, password):
    i=0
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('连接WIFI...')
    wlan.connect(essid, password)
    while not wlan.isconnected():
        i=i+1
        if(i>100000):
            return 0
    print('网络配置信息：', wlan.ifconfig())
    return 1
